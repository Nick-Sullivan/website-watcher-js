# Regular scraping

resource "aws_cloudwatch_event_rule" "regular_scrapes_for_all_users" {
  name                = "${local.prefix}-RegularScrapesForAllUsers"
  description         = "Regularly scrape"
  schedule_expression = "rate(6 hours)"
}

resource "aws_cloudwatch_event_target" "regular_scrapes_for_all_users" {
  rule      = aws_cloudwatch_event_rule.regular_scrapes_for_all_users.name
  target_id = "InvokeTransformLambda"
  arn       = aws_lambda_function.schedule_scrapes_for_all_users.arn
  retry_policy {
    maximum_retry_attempts       = 0
    maximum_event_age_in_seconds = 60 * 60
  }
}

resource "aws_lambda_permission" "regular_scrapes_for_all_users" {
  statement_id  = "RegularScrapesForAllUsers"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.schedule_scrapes_for_all_users.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.regular_scrapes_for_all_users.arn
}

# Adhoc scraping

resource "aws_cloudwatch_event_rule" "adhoc_scrapes_for_all_users" {
  name          = "${local.prefix}-AdhocScrapesForAllUsers"
  description   = "Adhoc scrape"
  event_pattern = <<EOF
{
    "detail-type": ["${title(var.environment)}-ScrapesForAllUsersRequested"]
}
EOF
}

resource "aws_cloudwatch_event_target" "adhoc_scrapes_for_all_users" {
  rule      = aws_cloudwatch_event_rule.adhoc_scrapes_for_all_users.name
  target_id = "InvokeTransformLambda"
  arn       = aws_lambda_function.schedule_scrapes_for_all_users.arn
  retry_policy {
    maximum_retry_attempts       = 0
    maximum_event_age_in_seconds = 60 * 60
  }
}

resource "aws_lambda_permission" "adhoc_scrapes_for_all_users" {
  statement_id  = "AdhocScrapesForAllUsers"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.schedule_scrapes_for_all_users.arn
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.adhoc_scrapes_for_all_users.arn
}
