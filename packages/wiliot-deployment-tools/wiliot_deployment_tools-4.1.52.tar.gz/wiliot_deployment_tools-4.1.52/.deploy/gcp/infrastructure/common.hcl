# Common variables for all GCP projects
locals {
  # Prefix for the resource naming
  name_prefix = "wiliot"

  # Global domain
  domain = "gcp.wiliot.cloud"

  # Terraform label name for the resource tagging
  terraform_fingerprint = "terraform"

  default_region = "us-central1"

  # All the GCP Project IDs
  projects = {
    dev   = "wiliot-dev-376415",
    test  = "wiliot-test",
    prod  = "wiliot-prod",
    infra = "wiliot-infra",
    audit = "wiliot-audit"
  }

  # Team responsible for the service
  team = "SRE"

  # Deploy cloud
  cloud = "GCP"

  app_name     = "pywiliot-deployment-tools"
  app_gar_repo = "us-central1-docker.pkg.dev/wiliot-infra/docker"
  app_tag      = lower(get_env("CLOUD_VERSION", ""))
  app_image    = "${local.app_gar_repo}/${local.app_name}"

  #  # Istio gateways
  #  istio_mqtt_gateway    = "istio-system/public-mqtt-gw"
  #  istio_public_gateway  = "istio-system/public-gw"
  #  istio_private_gateway = "istio-system/private-gw"

  # Prefix for the databricks resources
  databricks_prefix = "dbc"

  # Common tags set
  tags = {
    "Owner" = local.terraform_fingerprint
    "App"   = local.app_name
    "Team"  = local.team
  }
}
