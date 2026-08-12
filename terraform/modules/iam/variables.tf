variable "role_name" {
  description = "Name of the IAM role."
  type        = string
}

variable "bucket_arn" {
  description = "ARN of the S3 bucket."
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources."
  type        = map(string)
  default     = {}
}

#variable "lambda_role_name" {
#  description = "Name of the IAM role for Lambda."
#  type        = string
#}

#variable "s3_bucket_name" {
#  description = "Name of the S3 bucket for which the role should get access."
#  type        = string
#}
