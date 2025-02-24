locals {
  # Load common vars
  common_vars = read_terragrunt_config(find_in_parent_folders("common.hcl"))

  # Automatically load account-level variables
  project_vars = read_terragrunt_config(find_in_parent_folders("project.hcl"))

  # Automatically load region-level variables
  region_vars = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  default_region = local.region_vars.locals.default_region
  project_name   = local.project_vars.locals.project_name
  project_id     = local.common_vars.locals.projects[local.project_name]
  app_name       = local.common_vars.locals.app_name
}

generate "provider" {
  path      = "provider.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
provider "google" {
  project = "${local.project_id}"
}
EOF
}

remote_state {
  backend = "gcs"
  config = {
    bucket   = "bkt-wiliot-tf-state"
    prefix   = "${local.app_name}/${path_relative_to_include()}/terraform.tfstate"
    project  = local.project_id
    location = local.common_vars.locals.default_region
  }
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
}

inputs = local.common_vars.locals

terragrunt_version_constraint = "~> 0.50.17"
