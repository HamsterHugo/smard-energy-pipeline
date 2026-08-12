module "data_bucket" {
  source = "./modules/s3"

  bucket_name = "${local.name_prefix}-data-bucket-${local.account_id}"
  layer_zip   = "${path.root}/../aws/layer.zip"
  tags        = local.common_tags
  public      = true
}

module "iam" {
  source = "./modules/iam"

  role_name  = local.iam_role_name
  bucket_arn = module.data_bucket.bucket_arn
  tags       = local.common_tags
}

module "lambda_layer" {
  source       = "./modules/lambda_layer"
  bucket_id    = module.data_bucket.bucket_id
  layer_s3_key = module.data_bucket.layer_s3_key
  layer_name   = "${local.name_prefix}-layer"
}

module "lambda_ingest" {
  source        = "./modules/lambda"
  function_name = "${local.name_prefix}-ingest"
  source_dir    = "${path.root}/../aws/lambda/ingest"
  role_arn      = module.iam.role_arn
  layer_arn     = module.lambda_layer.layer_arn
  tags          = local.common_tags
}

module "lambda_query" {
  source        = "./modules/lambda"
  function_name = "${local.name_prefix}-query"
  source_dir    = "${path.root}/../aws/lambda/query"
  role_arn      = module.iam.role_arn
  layer_arn     = module.lambda_layer.layer_arn
  tags          = local.common_tags
}

module "api_gateway" {
  source               = "./modules/api_gateway"
  api_name             = "${local.name_prefix}-api"
  lambda_invoke_arn    = module.lambda_query.invoke_arn
  lambda_function_name = module.lambda_query.function_name
  tags                 = local.common_tags
}

module "eventbridge" {
  source               = "./modules/eventbridge"
  rule_name            = "${local.name_prefix}-daily-ingest"
  lambda_arn           = module.lambda_ingest.function_arn
  lambda_function_name = module.lambda_ingest.function_name
  tags                 = local.common_tags
}

#module "iam" {
#  source = "./modules/iam"
#
#  lambda_role_name = local.iam_role_name
#  s3_bucket_name   = "${local.name_prefix}-data-bucket-${local.account_id}"
#}


#module "lambda_ingest" {
#  source = "./modules/lambda"

#  lambda_role_name = local.iam_role_name
#  function_name    = "${local.name_prefix}-ingest"
#  source_dir       = "${path.root}/../aws/lambda/ingest"
#  bucket_name      = module.data_bucket.bucket_id
#  tags             = local.common_tags
#}

#module "lambda_query" {
#  source = "./modules/lambda"
#
#  lambda_role_name = local.iam_role_name
#  function_name    = "${local.name_prefix}-query"
#  source_dir       = "${path.root}/../aws/lambda/query"
#  bucket_name      = module.data_bucket.bucket_id
#  tags             = local.common_tags
#}

#module "api_gateway" {
#  source = "./modules/api_gateway"
#
#  api_name             = "${local.name_prefix}-api"
#  lambda_invoke_arn    = module.lambda_query.invoke_arn
#  lambda_function_name = module.lambda_query.function_name
#  tags                 = local.common_tags
#}

#module "eventbridge" {
#  source = "./modules/eventbridge"
#
#  rule_name            = "${local.name_prefix}-daily-ingest"
#  lambda_arn           = module.lambda_ingest.function_arn
#  lambda_function_name = module.lambda_ingest.function_name
#  tags                 = local.common_tags
#}