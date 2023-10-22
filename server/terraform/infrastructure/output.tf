output "gateway_url" {
  description = "URL for invoking API Gateway."
  value       = aws_api_gateway_stage.gateway.invoke_url
}

resource "aws_ssm_parameter" "api_gateway_url" {
  name  = "${local.prefix_parameter}/ApiGateway/Url"
  type  = "String"
  value = aws_api_gateway_stage.gateway.invoke_url
}

resource "aws_ssm_parameter" "automated_tester_password" {
  name  = "${local.prefix_parameter}/AutomatedTester/Password"
  type  = "SecureString"
  value = random_password.automated_tester_password.result
}

resource "aws_ssm_parameter" "automated_tester_username" {
  name  = "${local.prefix_parameter}/AutomatedTester/Username"
  type  = "String"
  value = local.automated_tester_username
}

resource "aws_ssm_parameter" "sqs_url" {
  name  = "${local.prefix_parameter}/Sqs/Url"
  type  = "SecureString"
  value = aws_sqs_queue.scrape_queue.url
}
