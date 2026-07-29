locals {
  name_prefix = "smard-energy-pipeline"
  account_id = data.aws_caller_identity.current.account_id

  common_tags = {
    Owner = var.owner
    Project = "smard-energy-pipeline"
    Environment = var.environment
    ManagedBy = "terraform"
  }
}