locals {
  name_prefix = "smard-energy-pipeline"

  common_tags = {
    Owner = var.owner
    Project = "smard-energy-pipeline"
    Environment = var.environment
    ManagedBy = "terraform"
  }
}