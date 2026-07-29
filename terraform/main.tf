module "data_bucket" {
  source = "./modules/s3"

  bucket_name = "${local.name_prefix}_data_bucket_${formatdate("YYYY-MM-DD", timestamp())}"
  tags        = local.common_tags
}