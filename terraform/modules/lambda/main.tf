data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = var.source_dir
  output_path = "${path.module}/tmp/${var.function_name}.zip"
}

resource "aws_lambda_function" "function" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = var.function_name
  role             = var.role_arn
  handler          = var.handler
  runtime          = var.runtime
  timeout          = var.timeout
  memory_size      = var.memory_size
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  layers           = [var.layer_arn]

  environment {
    variables = var.environment_variables
  }

  tags = var.tags
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 7
  tags              = var.tags
}

#data "aws_iam_role" "lambda_role" {
#  name = var.lambda_role_name
#}

# ZIP file for the lambda layer
#data "archive_file" "layer_zip" {
#  type        = "zip"
#  source_file = "${path.root}/../layer.zip"
#  output_path = "${path.module}/tmp/layer.zip"
#}

# Load ZIP file into the S3 bucket.
#resource "aws_s3_object" "layer_zip" {
#  bucket = var.bucket_name
#  key    = "layer.zip"
#  source = data.archive_file.layer_zip.output_path
#  etag   = filemd5(data.archive_file.layer_zip.output_path)
#}

# Create Lambda-Layer from the S3 bucket.
#resource "aws_lambda_layer_version" "smard_layer" {
#  s3_bucket           = aws_s3_object.layer_zip.bucket
#  s3_key              = aws_s3_object.layer_zip.key
#  layer_name          = "smard-pipeline-layer"
#  compatible_runtimes = ["python3.12"]
#}

# Lambda function
#resource "aws_lambda_function" "function" {
#  filename         = data.archive_file.lambda_zip.output_path
#  function_name    = var.function_name
#  role             = module.iam.lambda_role_arn
#  handler          = var.handler
#  runtime          = var.runtime
#  timeout          = var.timeout
#  memory_size      = var.memory_size
#  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
#  layers           = [aws_lambda_layer_version.smard_layer.arn]
#
#  environment {
#    variables = var.environment_variables
#  }
#
#  tags = var.tags
#}

# CloudWatch Log group for the lambda function.
#resource "aws_cloudwatch_log_group" "lambda_logs" {
#  name              = "/aws/lambda/${var.function_name}"
#  retention_in_days = 7
#  tags              = var.tags
#}