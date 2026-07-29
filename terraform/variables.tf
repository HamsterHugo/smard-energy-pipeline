variable "aws_region" {
  description = "AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "owner" {
  description = "The name of the owner of the resource."
  type        = string
}