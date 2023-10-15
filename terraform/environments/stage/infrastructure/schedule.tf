resource "aws_cloudwatch_event_rule" "schedule_scrapes" {
  name                = "${local.prefix}-ScheduleScrapes"
  description         = "Regularly scrape"
  schedule_expression = "rate(6 hours)"
}

# resource "aws_cloudwatch_event_target" "schedule_scrapes" {
#   rule      = aws_cloudwatch_event_rule.schedule_scrapes.name
#   target_id = "InvokeTransformLambda"
#   arn       = aws_lambda_function.schedule_scrapes.arn
#   retry_policy {
#     maximum_retry_attempts       = 0
#     maximum_event_age_in_seconds = 60 * 60
#   }
# }

resource "aws_lambda_permission" "schedule_scrapes" {
  statement_id  = "AllowExecutionFromEventBus"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.schedule_scrapes.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule_scrapes.arn
}
