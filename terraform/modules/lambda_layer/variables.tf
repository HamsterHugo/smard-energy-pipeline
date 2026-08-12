variable "bucket_id" {
  description = "ID of the S3 bucket containing the layer ZIP."
  type        = string
}

variable "layer_s3_key" {
  description = "S3 key of the layer ZIP file."
  type        = string
}

variable "layer_name" {
  description = "Name of the Lambda Layer."
  type        = string
}

variable "compatible_runtimes" {
  description = "Compatible runtimes for the layer."
  type        = list(string)
  default     = ["python3.12"]
}