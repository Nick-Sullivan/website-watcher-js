output "gateway_url" {
  description = "URL for invoking API Gateway."
  value       = aws_api_gateway_stage.gateway.invoke_url
}

resource "aws_ssm_parameter" "api_gateway_url" {
  name  = "${local.prefix_upper}_API_GATEWAY_URL"
  type  = "String"
  value = aws_api_gateway_stage.gateway.invoke_url
}

resource "aws_ssm_parameter" "automated_tester_username" {
  name  = "${local.prefix_upper}_AUTOMATED_TESTER_USERNAME"
  type  = "String"
  value = local.automated_tester_username
}

resource "aws_ssm_parameter" "automated_tester_password" {
  name  = "${local.prefix_upper}_AUTOMATED_TESTER_PASSWORD"
  type  = "SecureString"
  value = random_password.automated_tester_password.result
}

# resource "local_file" "website" {
#   content  = <<-EOT
#         # This file is automatically generated by terraform
#         NEXT_PUBLIC_API_GATEWAY_URL="${aws_api_gateway_stage.gateway.invoke_url}"
#         NEXT_PUBLIC_COGNITO_USER_POOL_ID="${data.aws_ssm_parameter.cognito_user_pool_id.value}"
#         NEXT_PUBLIC_COGNITO_CLIENT_ID="${data.aws_ssm_parameter.cognito_client_id.value}"
#         NEXT_PUBLIC_COGNITO_REGION="ap-southeast-2"
#     EOT
#   filename = "${local.website_dir}/.env"
# }

# resource "local_file" "terraform" {
#   content  = <<-EOT
#         API_GATEWAY_URL=${aws_api_gateway_stage.gateway.invoke_url}
#         AUTOMATED_TESTER_USERNAME=${local.automated_tester_username}
#         AUTOMATED_TESTER_PASSWORD=${random_password.automated_tester_password.result}
#         COGNITO_USER_POOL=${data.aws_ssm_parameter.cognito_user_pool_id.value}
#         COGNITO_CLIENT_ID=${data.aws_ssm_parameter.cognito_client_id.value}
#     EOT
#   filename = "output.env"
# }
