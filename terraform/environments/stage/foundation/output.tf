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
  name  = "${local.prefix_upper}_S3_NAME"
  type  = "String"
  value = aws_s3_bucket.watch_results.bucket
}

resource "aws_ssm_parameter" "cognito_client_id" {
  name  = "${local.prefix_upper}_COGNITO_CLIENT_ID"
  type  = "String"
  value = aws_cognito_user_pool_client.users.id
}

resource "aws_ssm_parameter" "cognito_region" {
  name  = "${local.prefix_upper}_COGNITO_REGION"
  type  = "String"
  value = "ap-southeast-2"
}

resource "aws_ssm_parameter" "cognito_user_pool_arn" {
  name  = "${local.prefix_upper}_COGNITO_USER_POOL_ARN"
  type  = "String"
  value = aws_cognito_user_pool.users.arn
}

resource "aws_ssm_parameter" "cognito_user_pool_id" {
  name  = "${local.prefix_upper}_COGNITO_USER_POOL_ID"
  type  = "String"
  value = aws_cognito_user_pool.users.id
}

resource "aws_ssm_parameter" "ecr_name" {
  name  = "${local.prefix_upper}_ECR_NAME"
  type  = "String"
  value = aws_ecr_repository.lambda_base.name
}

resource "aws_ssm_parameter" "ecr_url" {
  name  = "${local.prefix_upper}_ECR_URL"
  type  = "String"
  value = aws_ecr_repository.lambda_base.repository_url
}

resource "aws_ssm_parameter" "s3_snapshot_arn" {
  name  = "${local.prefix_upper}_S3_SNAPSHOT_ARN"
  type  = "String"
  value = aws_s3_bucket.watch_results.arn
}

resource "aws_ssm_parameter" "s3_snapshot_name" {
  name  = "${local.prefix_upper}_S3_SNAPSHOT_NAME"
  type  = "String"
  value = aws_s3_bucket.watch_results.bucket
}

// Write out variables for use in other terraforms
# "automated_tester_username": "${local.automated_tester_username}",
# "automated_tester_password": "${random_password.automated_tester_password.result}",

# resource "local_file" "terraform" {
#   content  = <<-EOT
#     {
#         "cognito_client_id": "${aws_cognito_user_pool_client.users.id}",
#         "cognito_client_secret": "${aws_cognito_user_pool_client.users.client_secret}",
#         "cognito_user_pool_id": "${aws_cognito_user_pool.users.id}",
#         "cognito_user_pool_arn": "${aws_cognito_user_pool.users.arn}",
#         "ecr_name": "${aws_ecr_repository.lambda_base.name}",
#         "ecr_url": "${aws_ecr_repository.lambda_base.repository_url}",
#         "s3_snapshot_arn": "${aws_s3_bucket.watch_results.arn}",
#         "s3_snapshot_name": "${aws_s3_bucket.watch_results.bucket}"
#     }
#     EOT
#   filename = "output.json"
# }
