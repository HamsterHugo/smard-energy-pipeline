output "bucket_name" {
  value = module.data_bucket.bucket_id
}

output "website_url" {
  value = module.data_bucket.website_url
}

output "api_url" {
  value = module.api_gateway.api_url
}