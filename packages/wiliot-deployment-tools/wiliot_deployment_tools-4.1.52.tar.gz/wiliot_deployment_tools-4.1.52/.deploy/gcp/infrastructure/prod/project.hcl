# Set account variables
locals {
  common_vars = read_terragrunt_config(find_in_parent_folders("common.hcl"))

  project_name        = "prod"
  project_domain_name = "${local.project_name}.${local.common_vars.locals.domain}"
  gke_cluster_name    = "${local.common_vars.locals.name_prefix}-${local.project_name}"

  # Set the account-wide tags
  tags = merge({
    "Environment" = local.project_name
  }, local.common_vars.locals.tags)
}
