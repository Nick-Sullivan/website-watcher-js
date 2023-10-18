data "aws_caller_identity" "identity" {}


data "aws_ssm_parameter" "api_gateway_url" {
  name = "${local.prefix_upper}_API_GATEWAY_URL"
}

data "aws_ssm_parameter" "cognito_client_id" {
  name = "${local.prefix_upper}_COGNITO_CLIENT_ID"
}

data "aws_ssm_parameter" "cognito_user_pool_id" {
  name = "${local.prefix_upper}_COGNITO_USER_POOL_ID"
}

data "aws_ssm_parameter" "cognito_region" {
  name = "${local.prefix_upper}_COGNITO_REGION"
}
