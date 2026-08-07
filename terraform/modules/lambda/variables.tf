variable "function_name" {
  description = "Nsme of the Lambda function."
  type        = string
}

variable "handler" {
  description = "Handler for the Lambda function."
  type        = string
  default     = "handler.lambda_handler"
}

variable "runtime" {
  description = "Runtime for the Lambda function."
  type        = string
  default     = "python3.12"
}

variable "timeout" {
  description = "Timeout for the Lambda function in seconds."
  type        = number
  default     = 300
}

variable "memory_size" {
  description = "Memory size for the Lambda function in MB."
  type        = number
  default     = 256
}

variable "source_dir" {
  description = "Path to the Lmabda function source directory."
  type        = string
}

variable "environment_variables" {
  description = "Environmen variables for the Lambda function."
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Tags to apply to the Lambda function."
  type        = map(string)
  default     = {}
}