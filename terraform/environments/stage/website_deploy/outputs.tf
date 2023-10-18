output "website_endpoint" {
  description = "Website URL from public S3 bucket."
  value       = aws_s3_bucket_website_configuration.website.website_endpoint
}

resource "aws_ssm_parameter" "website_url" {
  name  = "${local.prefix_upper}_WEBSITE_URL"
  type  = "String"
  value = aws_s3_bucket_website_configuration.website.website_endpoint
}
