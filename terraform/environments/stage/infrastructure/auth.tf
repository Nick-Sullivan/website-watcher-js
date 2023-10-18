resource "random_password" "automated_tester_password" {
  length  = 16
  special = false
}

resource "aws_cognito_user" "automated_tester" {
  user_pool_id   = data.aws_ssm_parameter.cognito_user_pool_id.value
  username       = local.automated_tester_username
  password       = random_password.automated_tester_password.result
  message_action = "SUPPRESS"
  attributes = {
    email          = local.automated_tester_username
    email_verified = true
  }
}
