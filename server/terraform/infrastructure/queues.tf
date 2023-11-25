resource "aws_sqs_queue" "scrape_queue" {
  name                       = "${local.prefix}-ScrapeQueue"
  message_retention_seconds  = 12 * 60 * 60
  visibility_timeout_seconds = 60
  receive_wait_time_seconds = 20  # to reduce the number of empty receives
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.scrape_dead_letter.arn
    maxReceiveCount     = 1
  })
}

resource "aws_sqs_queue" "scrape_dead_letter" {
  name                      = "${local.prefix}-ScrapeQueueFailed"
  message_retention_seconds = 14 * 24 * 60 * 60
}

resource "aws_sqs_queue_redrive_allow_policy" "scrape_queue" {
  queue_url = aws_sqs_queue.scrape_dead_letter.id

  redrive_allow_policy = jsonencode({
    redrivePermission = "byQueue",
    sourceQueueArns   = [aws_sqs_queue.scrape_queue.arn]
  })
}

resource "aws_lambda_event_source_mapping" "scrape_queue" {
  event_source_arn = aws_sqs_queue.scrape_queue.arn
  function_name    = aws_lambda_function.scrape_website.function_name
  batch_size       = 1
}
