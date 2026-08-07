variable "rule_name" {
  description = "Name of the EventBridge rule."
  type        = string
}

variable "schedule_expression" {
  description = "Schedule expression for the EventBridge rule."
  type        = string
  default     = "cron(0 2 * * ? *)"
}

variable "lambda_arn" {
  description = "ARN of the Lambda function to trigger."
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda function."
  type        = string
}

variable "tags" {
  description = "Tags to aplpy to the EventBridge rule."
  type        = map(string)
  default     = {}
}