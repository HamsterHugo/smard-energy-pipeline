resource "aws_lambda_layer_version" "layer" {
  s3_bucket           = var.bucket_id
  s3_key              = var.layer_s3_key
  layer_name          = var.layer_name
  compatible_runtimes = var.compatible_runtimes
}