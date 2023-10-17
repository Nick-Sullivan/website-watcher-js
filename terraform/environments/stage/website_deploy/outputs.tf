output "website_endpoint" {
  description = "Website URL from public S3 bucket."
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}
