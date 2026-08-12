variable "api_name" {
  description = "Name of the API Gateway."
  type        = string
}

variable "lambda_invoke_arn" {
  description = "Invoke ARN of the Lambda Query function."
  type        = string
}

variable "lambda_function_name" {
  description = "Name of the Lambda Query function."
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources."
  type        = map(string)
  default     = {}
}

#variable "api_name" {
#  description = "Name of the API Gateway."
#  type        = string
#}

#variable "lambda_invoke_arn" {
#  description = "Invoke ARN of the Lambda function."
#  type        = string
#}

#variable "lambda_function_name" {
#  description = "Name of the Lambda function."
#  type        = string
#}

#variable "tags" {
#  description = "Tags to apply to the API Gateway."
#  type        = map(string)
#  default     = {}
#}