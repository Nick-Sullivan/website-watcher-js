data "aws_caller_identity" "identity" {}


data "aws_ssm_parameter" "cognito_client_id" {
  name = "${local.prefix_upper}_COGNITO_CLIENT_ID"
}

data "aws_ssm_parameter" "cognito_user_pool_arn" {
  name = "${local.prefix_upper}_COGNITO_USER_POOL_ARN"
}

data "aws_ssm_parameter" "cognito_user_pool_id" {
  name = "${local.prefix_upper}_COGNITO_USER_POOL_ID"
}

data "aws_ssm_parameter" "ecr_name" {
  name = "${local.prefix_upper}_ECR_NAME"
}

data "aws_ssm_parameter" "ecr_url" {
  name = "${local.prefix_upper}_ECR_URL"
}

data "aws_ssm_parameter" "s3_name" {
  name = "${local.prefix_upper}_S3_NAME"
}

data "aws_ssm_parameter" "s3_snapshot_arn" {
  name = "${local.prefix_upper}_S3_SNAPSHOT_ARN"
}

data "aws_ssm_parameter" "s3_snapshot_name" {
  name = "${local.prefix_upper}_S3_SNAPSHOT_NAME"
}
