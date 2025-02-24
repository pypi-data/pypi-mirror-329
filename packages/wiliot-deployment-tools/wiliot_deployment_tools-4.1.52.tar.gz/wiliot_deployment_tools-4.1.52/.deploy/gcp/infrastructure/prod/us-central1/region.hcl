# Set region variables
locals {
  project_vars       = read_terragrunt_config(find_in_parent_folders("project.hcl"))
  default_region     = "us-central1"
  region_domain_name = "${local.default_region}.${local.project_vars.locals.project_domain_name}"
}
