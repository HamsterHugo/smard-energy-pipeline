variable "function_name" {
  description = "Name of the Lambda function."
  type        = string
}

variable "handler" {
  description = "Handler for the Lambda fucntion."
  type        = string
  default     = "handler.lambda_handler"
}

variable "runtime" {
  description = "Runtime for the Lambda function."
  type        = string
  default     = "python3.12"
}

variable "timeout" {
  description = "Timeout in seconds."
  type        = number
  default     = 300
}

variable "memory_size" {
  description = "Memory size in MB."
  type        = number
  default     = 256
}

variable "source_dir" {
  description = "Path to the Lambda function source directory."
  type        = string
}

variable "role_arn" {
  description = "ARN of the IAM role."
  type        = string
}

variable "layer_arn" {
  description = "ARN of the Lambda Layer."
  type        = string
}

variable "environment_variables" {
  description = "Environment variables for the Lambda function."
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Tags to apply to all resources."
  type        = map(string)
  default     = {}
}
