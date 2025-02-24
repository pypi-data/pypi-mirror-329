include {
  path = find_in_parent_folders()
}

terraform {
  source = "git::git@bitbucket.org:wiliot/wiliot-cloud-modules.git//common/databricks/clusters"
}

generate "data" {
  path      = "data.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
data "google_secret_manager_secret_version" "this" {
  secret = "databricks"
}

locals {
  app_secrets = jsondecode(
    data.google_secret_manager_secret_version.this.secret_data
  )
  host = local.app_secrets["host"]
  token = local.app_secrets["token"]
}

provider "databricks" {
  host                   = local.host
  token                  = local.token
}
EOF
}

locals {
  # Automatically load common variables shared across all projects
  common_vars = read_terragrunt_config(find_in_parent_folders("common.hcl"))

  # Extract the name prefix for easy access
  name_prefix = local.common_vars.locals.name_prefix

  # Automatically load account-level variables
  project_vars = read_terragrunt_config(find_in_parent_folders("project.hcl"))

  # Automatically load region-level variables
  region_vars = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  # Extract the account_name for easy access
  project_name = local.project_vars.locals.project_name

  project_id = local.common_vars.locals.projects[local.project_name]

  # Extract the region for easy access
  gcp_region = local.region_vars.locals.default_region

  # Extract the EKS cluster name for easy access
  gke_cluster_name = "${local.project_vars.locals.gke_cluster_name}-${local.region_vars.locals.default_region}"

  # Extract region_domain_name for easy access
  region_domain_name = local.region_vars.locals.region_domain_name

  # Automatically load Databricks variables
  databricks_vars = read_terragrunt_config(find_in_parent_folders("dbc.hcl"))
}


inputs = {
  group_name = "team_network_system"
  clusters = {
    system-network = {
      spark_version = "14.3.x-scala2.12",
      spark_conf = {
        "spark.databricks.cluster.profile"          = "singleNode",
        "spark.executor.processTreeMetrics.enabled" = "true",
        "spark.master"                              = "local[*]",
        "spark.ui.prometheus.enabled"               = "true",
        "spark.sql.streaming.metricsEnabled"        = "true"
      },
      gcp_attributes = {
        zone_id                = "HA"
        google_service_account = "${local.databricks_vars.locals.google_service_account}"
      }
      node_type_id            = "e2-standard-4",
      driver_node_type_id     = "e2-standard-4",
      autotermination_minutes = 60,
      init_scripts = [
        {
          gcs = {
            destination = format("gs://wiliot-%s-%s-monitoring-and-logging/monitoring/init-scripts/initialize-metrics-v2.sh", local.project_name, local.gcp_region)
          }
        },
        {
          gcs = {
            destination = format("gs://wiliot-%s-%s-monitoring-and-logging/clusters/init-scripts/system-network/install_packages.sh", local.project_name, local.gcp_region)
          }
        },
      ],
      policy_id          = "946445837F000123"
      data_security_mode = "NONE",
      runtime_engine     = "STANDARD"
      num_workers        = 0,
      custom_tags = {
        ResourceClass = "SingleNode"
        environment   = local.project_name
        gcp_region    = local.gcp_region
      }
    }
  }
}
