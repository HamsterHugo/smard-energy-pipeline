variable "bucket_name" {
  description = "Full name of the bucket to create."
  type = string
}

variable "tags" {
  description = "Tags to apply to the bucket."
  type = map(string)
  default = {}
}