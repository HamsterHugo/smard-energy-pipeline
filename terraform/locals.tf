data "aws_caller_identity" "current" {}

locals {
  name_prefix   = "smard-energy-pipeline"
  account_id    = data.aws_caller_identity.current.account_id
  iam_role_name = "smard-lambda-role"

  common_tags = {
    Owner       = var.owner
    Project     = "smard-energy-pipeline"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}