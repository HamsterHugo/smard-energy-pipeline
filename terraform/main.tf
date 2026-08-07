data "aws_caller_identity" "current" {}

module "data_bucket" {
  source      = "./modules/s3"
  bucket_name = "${local.name_prefix}-data-bucket-${local.account_id}"
  tags        = local.common_tags
  public      = true
}

module "lambda_ingest" {
  source        = "./modules/lambda"
  function_name = "${local.name_prefix}-ingest"
  source_dir    = "${path.root}/../aws/lambda/ingest"
  tags          = local.common_tags
}

module "lambda_query" {
  source        = "./modules/lambda"
  function_name = "${local.name_prefix}-query"
  source_dir    = "${path.root}/../aws/lambda/query"
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