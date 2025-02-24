locals {
  common_vars  = read_terragrunt_config(find_in_parent_folders("common.hcl"))
  project_vars = read_terragrunt_config(find_in_parent_folders("project.hcl"))

  google_service_account = "databricks-clusters-sa@wiliot-prod.iam.gserviceaccount.com"

  tags = merge({
    "System" = "Databricks"
  }, local.project_vars.locals.tags)
}
