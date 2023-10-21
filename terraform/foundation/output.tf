output "s3_name" {
  description = "Name of the S3 bucket holding watch result images"
  value       = aws_s3_bucket.watch_results.bucket
}

output "cognito_client_id" {
  description = "ID of the Cognito client"
  value       = aws_cognito_user_pool_client.users.id
}

output "cognito_user_pool_arn" {
  description = "ARN of the Cognito user pool"
  value       = aws_cognito_user_pool.users.arn
}

output "cognito_user_pool_id" {
  description = "ID of the Cognito user pool"
  value       = aws_cognito_user_pool.users.id
}

output "ecr_name" {
  description = "Name of the ECR repository"
  value       = aws_ecr_repository.lambda_base.name
}

output "ecr_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.lambda_base.repository_url
}

output "s3_snapshot_arn" {
  description = "ARN of the S3 bucket holding snapshots"
  value       = aws_s3_bucket.watch_results.arn
}

output "s3_snapshot_name" {
  description = "Name of the S3 bucket holding snapshots"
  value       = aws_s3_bucket.watch_results.bucket
}

resource "aws_ssm_parameter" "s3_name" {
  name  = "${local.prefix_parameter}/S3/Name"
  type  = "String"
  value = aws_s3_bucket.watch_results.bucket
}

resource "aws_ssm_parameter" "cognito_client_id" {
  name  = "${local.prefix_parameter}/Cognito/ClientId"
  type  = "String"
  value = aws_cognito_user_pool_client.users.id
}

resource "aws_ssm_parameter" "cognito_region" {
  name  = "${local.prefix_parameter}/Cognito/Region"
  type  = "String"
  value = "ap-southeast-2"
}

resource "aws_ssm_parameter" "cognito_user_pool_arn" {
  name  = "${local.prefix_parameter}/Cognito/UserPool/Arn"
  type  = "String"
  value = aws_cognito_user_pool.users.arn
}

resource "aws_ssm_parameter" "cognito_user_pool_id" {
  name  = "${local.prefix_parameter}/Cognito/UserPool/Id"
  type  = "String"
  value = aws_cognito_user_pool.users.id
}

resource "aws_ssm_parameter" "db_scrape_arn" {
  name  = "${local.prefix_parameter}/Db/Scrape/Arn"
  type  = "String"
  value = aws_dynamodb_table.websites.arn
}

resource "aws_ssm_parameter" "db_scrape_name" {
  name  = "${local.prefix_parameter}/Db/Scrape/Name"
  type  = "String"
  value = aws_dynamodb_table.websites.name
}

resource "aws_ssm_parameter" "db_website_arn" {
  name  = "${local.prefix_parameter}/Db/Website/Arn"
  type  = "String"
  value = aws_dynamodb_table.websites.arn
}

resource "aws_ssm_parameter" "db_website_name" {
  name  = "${local.prefix_parameter}/Db/Website/Name"
  type  = "String"
  value = aws_dynamodb_table.websites.name
}

resource "aws_ssm_parameter" "ecr_name" {
  name  = "${local.prefix_parameter}/Ecr/Name"
  type  = "String"
  value = aws_ecr_repository.lambda_base.name
}

resource "aws_ssm_parameter" "ecr_url" {
  name  = "${local.prefix_parameter}/Ecr/Url"
  type  = "String"
  value = aws_ecr_repository.lambda_base.repository_url
}

resource "aws_ssm_parameter" "s3_snapshot_arn" {
  name  = "${local.prefix_parameter}/S3/Snapshot/Arn"
  type  = "String"
  value = aws_s3_bucket.watch_results.arn
}

resource "aws_ssm_parameter" "s3_snapshot_name" {
  name  = "${local.prefix_parameter}/S3/Snapshot/Name"
  type  = "String"
  value = aws_s3_bucket.watch_results.bucket
}
