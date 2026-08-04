data "aws_caller_identity" "current" {}

module "data_bucket" {
  source      = "./modules/s3"
  bucket_name = "${local.name_prefix}-data-bucket-${local.account_id}"
  tags        = local.common_tags
  public      = true
}