output "bucket_id" {
  value = aws_s3_bucket.bucket.id
}

output "bucket_arn" {
  value = aws_s3_bucket.bucket.arn
}

output "website_url" {
  value = aws_s3_bucket_website_configuration.website.website_endpoint #aws_s3_bucket_website_configuration.website[0].website_endpoint : null
}

output "layer_s3_key" {
  value = aws_s3_object.layer_zip.key
}