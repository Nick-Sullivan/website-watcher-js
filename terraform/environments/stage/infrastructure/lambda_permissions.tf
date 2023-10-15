

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "websites_db_query" {
  statement {
    actions = [
      "dynamodb:Query",
      "dynamodb:GetItem",
    ]
    effect = "Allow"
    resources = [
      aws_dynamodb_table.websites.arn,
    ]
  }
}

data "aws_iam_policy_document" "websites_db_put" {
  statement {
    actions = [
      "dynamodb:PutItem",
      "dynamodb:Query",
      "dynamodb:GetItem",
    ]
    effect = "Allow"
    resources = [
      aws_dynamodb_table.websites.arn,
    ]
  }
}

data "aws_iam_policy_document" "websites_db_delete" {
  statement {
    actions = [
      "dynamodb:DeleteItem",
    ]
    effect = "Allow"
    resources = [
      aws_dynamodb_table.websites.arn,
    ]
  }
}

data "aws_iam_policy_document" "scrape_db_query" {
  statement {
    actions = [
      "dynamodb:Query",
      "dynamodb:GetItem",
    ]
    effect = "Allow"
    resources = [
      aws_dynamodb_table.scrape.arn,
    ]
  }
}

data "aws_iam_policy_document" "scrape_db_put" {
  statement {
    actions = [
      "dynamodb:PutItem",
      "dynamodb:Query",
    ]
    effect = "Allow"
    resources = [
      aws_dynamodb_table.scrape.arn,
    ]
  }
}

data "aws_iam_policy_document" "scrape_db_delete" {
  statement {
    actions = [
      "dynamodb:DeleteItem",
    ]
    effect = "Allow"
    resources = [
      aws_dynamodb_table.scrape.arn,
    ]
  }
}

data "aws_iam_policy_document" "scrape_queue_upload" {
  statement {
    actions = [
      "sqs:SendMessage",
    ]
    effect = "Allow"
    resources = [
      aws_sqs_queue.scrape_queue.arn,
    ]
  }
}

data "aws_iam_policy_document" "scrape_queue_read" {
  statement {
    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
    ]
    effect = "Allow"
    resources = [
      aws_sqs_queue.scrape_queue.arn,
    ]
  }
}

data "aws_iam_policy_document" "upload_to_s3" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:PutObjectAcl",
    ]
    effect    = "Allow"
    resources = ["${local.foundation_output.s3_snapshot_arn}/*"]
  }
}

data "aws_iam_policy_document" "read_s3" {
  statement {
    actions = [
      "s3:GetObject",
    ]
    effect    = "Allow"
    resources = ["${local.foundation_output.s3_snapshot_arn}/*"]
  }
}

data "aws_iam_policy_document" "delete_s3" {
  statement {
    actions = [
      "s3:DeleteObject",
    ]
    effect    = "Allow"
    resources = ["${local.foundation_output.s3_snapshot_arn}/*"]
  }
}
