locals {
  common_vars          = read_terragrunt_config(find_in_parent_folders("common.hcl"))
  account_vars         = read_terragrunt_config(find_in_parent_folders("account.hcl"))
  instance_profile_arn = "arn:aws:iam::398723525701:instance-profile/wiliot-dbc-prod-general-instance-profile"

  dbc_mws_secret_arn   = "arn:aws:secretsmanager:us-east-2:096303741971:secret:global/databricks/dev-816yqj"

  tags = merge({
    "System" = "Databricks"
  }, local.account_vars.locals.tags)
}
