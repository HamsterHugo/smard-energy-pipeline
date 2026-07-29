data "aws_caller_identity" "current" {}

module "data_bucket" {
  source = "./modules/s3"

  bucket_name = "${local.name_prefix}_data_bucket_${local.account_id}"
  tags        = local.common_tags
}