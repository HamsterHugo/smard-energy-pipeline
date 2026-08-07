output "bucket_id" {
  value = aws_s3_bucket.s3_bucket.id
}

output "bucket_arn" {
  value = aws_s3_bucket.s3_bucket.arn
}

output "website_url" {
  value = var.public ? aws_s3_bucket_website_configuration.website[0].website_endpoint : null
}