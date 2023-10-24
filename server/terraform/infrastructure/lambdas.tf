
data "archive_file" "layer" {
  type        = "zip"
  source_dir  = "${local.lambda_dir}/layer"
  excludes    = ["__pycache__.py"]
  output_path = "${local.lambda_dir}/zip/layer.zip"
}

data "archive_file" "handler" {
  type        = "zip"
  source_dir  = "${local.lambda_dir}/handler"
  excludes    = ["__pycache__.py"]
  output_path = "${local.lambda_dir}/zip/handler.zip"
}

resource "aws_lambda_layer_version" "layer" {
  filename            = "${local.lambda_dir}/zip/layer.zip"
  layer_name          = "${local.prefix}-Layer"
  compatible_runtimes = ["python3.9"]
  source_code_hash    = data.archive_file.layer.output_base64sha256
}

resource "aws_cloudwatch_log_group" "all" {
  for_each          = local.lambda_names
  name              = "/aws/lambda/${each.value}"
  retention_in_days = 90
}

resource "aws_lambda_function" "create_website" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["create_website"]
  handler          = "create_website.create_website"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.create_website.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "WEBSITE_TABLE_NAME" : data.aws_ssm_parameter.db_website_name.value,
    }
  }
}

resource "aws_iam_role" "create_website" {
  name                = local.lambda_names["create_website"]
  description         = "Allows Lambda to create websites"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "S3WriteAccess"
    policy = data.aws_iam_policy_document.upload_to_s3.json
  }
  inline_policy {
    name   = "WriteToWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_put.json
  }
}

resource "aws_lambda_function" "delete_website" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["delete_website"]
  handler          = "delete_website.delete_website"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.delete_website.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "SCRAPE_TABLE_NAME" : data.aws_ssm_parameter.db_scrape_name.value,
      "SCREENSHOT_BUCKET_NAME" : data.aws_ssm_parameter.s3_snapshot_name.value,
      "WEBSITE_TABLE_NAME" : data.aws_ssm_parameter.db_website_name.value,
    }
  }
}

resource "aws_iam_role" "delete_website" {
  name                = local.lambda_names["delete_website"]
  description         = "Allows Lambda to delete websites and scrapes"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "DeleteWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_delete.json
  }
  inline_policy {
    name   = "QueryWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_query.json
  }
  inline_policy {
    name   = "DeleteScrapeDb"
    policy = data.aws_iam_policy_document.scrape_db_delete.json
  }
  inline_policy {
    name   = "QueryScrapeDb"
    policy = data.aws_iam_policy_document.scrape_db_query.json
  }
  inline_policy {
    name   = "DeleteScreenshotsS3"
    policy = data.aws_iam_policy_document.delete_s3.json
  }
}

resource "aws_lambda_function" "get_scrape" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["get_scrape"]
  handler          = "get_scrape.get_scrape"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.get_scrape.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "SCRAPE_TABLE_NAME" : data.aws_ssm_parameter.db_scrape_name.value,
    }
  }
}

resource "aws_iam_role" "get_scrape" {
  name                = local.lambda_names["get_scrape"]
  description         = "Allows Lambda to get a scrape"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "QueryScrapeDb"
    policy = data.aws_iam_policy_document.scrape_db_query.json
  }
}

resource "aws_lambda_function" "get_scrapes" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["get_scrapes"]
  handler          = "get_scrapes.get_scrapes"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.get_scrapes.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "SCRAPE_TABLE_NAME" : data.aws_ssm_parameter.db_scrape_name.value,
    }
  }
}

resource "aws_iam_role" "get_scrapes" {
  name                = local.lambda_names["get_scrapes"]
  description         = "Allows Lambda to get scrapes"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "QueryScrapeDb"
    policy = data.aws_iam_policy_document.scrape_db_query.json
  }
}

resource "aws_lambda_function" "get_screenshot" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["get_screenshot"]
  handler          = "get_screenshot.get_screenshot"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.get_screenshot.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "SCRAPE_TABLE_NAME" : data.aws_ssm_parameter.db_scrape_name.value,
      "SCREENSHOT_BUCKET_NAME" : data.aws_ssm_parameter.s3_snapshot_name.value,
    }
  }
}

resource "aws_iam_role" "get_screenshot" {
  name                = local.lambda_names["get_screenshot"]
  description         = "Allows Lambda to read screenshots"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "S3ReadAccess"
    policy = data.aws_iam_policy_document.read_s3.json
  }
  inline_policy {
    name   = "QueryScrapeDb"
    policy = data.aws_iam_policy_document.scrape_db_query.json
  }
}

resource "aws_lambda_function" "get_website" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["get_website"]
  handler          = "get_website.get_website"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.get_website.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "WEBSITE_TABLE_NAME" : data.aws_ssm_parameter.db_website_name.value,
    }
  }
}

resource "aws_iam_role" "get_website" {
  name                = local.lambda_names["get_website"]
  description         = "Allows Lambda to get a website"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "QueryWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_query.json
  }
}

resource "aws_lambda_function" "get_websites" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["get_websites"]
  handler          = "get_websites.get_websites"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.get_websites.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "WEBSITE_TABLE_NAME" : data.aws_ssm_parameter.db_website_name.value,
    }
  }
}

resource "aws_iam_role" "get_websites" {
  name                = local.lambda_names["get_websites"]
  description         = "Allows Lambda to list websites"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "QueryWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_query.json
  }
}

resource "aws_lambda_function" "preview" {
  package_type  = "Image"
  image_uri     = "${data.aws_ssm_parameter.ecr_url.value}@${data.aws_ecr_image.preview_docker_image.id}"
  function_name = local.lambda_names["preview"]
  role          = aws_iam_role.preview.arn
  memory_size   = 2048 # MB
  timeout       = 60
  depends_on = [
    aws_cloudwatch_log_group.all,
    terraform_data.preview_docker_push
  ]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "SCREENSHOT_BUCKET_NAME" : data.aws_ssm_parameter.s3_snapshot_name.value,
      "USES_PLAYWRIGHT" : "True",
    }
  }
}

resource "aws_iam_role" "preview" {
  name                = local.lambda_names["preview"]
  description         = "Allows Lambda run Playwright"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "S3WriteAccess"
    policy = data.aws_iam_policy_document.upload_to_s3.json
  }
}

resource "aws_lambda_function" "schedule_scrapes" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["schedule_scrapes"]
  handler          = "schedule_scrapes.schedule_scrapes"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.schedule_scrapes.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "SCRAPE_TABLE_NAME" : data.aws_ssm_parameter.db_scrape_name.value,
      "SQS_URL" : aws_sqs_queue.scrape_queue.url,
      "WEBSITE_TABLE_NAME" : data.aws_ssm_parameter.db_website_name.value,
    }
  }
}

resource "aws_iam_role" "schedule_scrapes" {
  name                = local.lambda_names["schedule_scrapes"]
  description         = "Allows Lambda to add messages to the scrape queue"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "QueryWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_query.json
  }
  inline_policy {
    name   = "QueryScrapeDb"
    policy = data.aws_iam_policy_document.scrape_db_query.json
  }
  inline_policy {
    name   = "UploadToScrapeQueue"
    policy = data.aws_iam_policy_document.scrape_queue_upload.json
  }
}


resource "aws_lambda_function" "schedule_scrapes_for_all_users" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["schedule_scrapes_for_all_users"]
  handler          = "schedule_scrapes_for_all_users.schedule_scrapes_for_all_users"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.schedule_scrapes_for_all_users.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "SCRAPE_TABLE_NAME" : data.aws_ssm_parameter.db_scrape_name.value,
      "SQS_URL" : aws_sqs_queue.scrape_queue.url,
      "WEBSITE_TABLE_NAME" : data.aws_ssm_parameter.db_website_name.value,
    }
  }
}

resource "aws_iam_role" "schedule_scrapes_for_all_users" {
  name                = local.lambda_names["schedule_scrapes_for_all_users"]
  description         = "Allows Lambda to add messages to the scrape queue"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "ScanWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_scan.json
  }
  inline_policy {
    name   = "QueryScrapeDb"
    policy = data.aws_iam_policy_document.scrape_db_query.json
  }
  inline_policy {
    name   = "UploadToScrapeQueue"
    policy = data.aws_iam_policy_document.scrape_queue_upload.json
  }
}


resource "aws_lambda_function" "scrape_website" {
  package_type  = "Image"
  image_uri     = "${data.aws_ssm_parameter.ecr_url.value}@${data.aws_ecr_image.scrape_docker_image.id}"
  function_name = local.lambda_names["scrape_website"]
  role          = aws_iam_role.scrape_website.arn
  memory_size   = 2048 # MB
  timeout       = 60
  depends_on = [
    aws_cloudwatch_log_group.all,
    terraform_data.scrape_docker_push
  ]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "SCRAPE_TABLE_NAME" : data.aws_ssm_parameter.db_scrape_name.value,
      "SCREENSHOT_BUCKET_NAME" : data.aws_ssm_parameter.s3_snapshot_name.value,
      "USES_PLAYWRIGHT" : "True",
      "WEBSITE_TABLE_NAME" : data.aws_ssm_parameter.db_website_name.value,
    }
  }
}

resource "aws_iam_role" "scrape_website" {
  name                = local.lambda_names["scrape_website"]
  description         = "Allows Lambda run Playwright"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "S3WriteAccess"
    policy = data.aws_iam_policy_document.upload_to_s3.json
  }
  inline_policy {
    name   = "QueryWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_query.json
  }
  inline_policy {
    name   = "WriteToScrapeDb"
    policy = data.aws_iam_policy_document.scrape_db_put.json
  }
  inline_policy {
    name   = "ReadFromScrapeQueue"
    policy = data.aws_iam_policy_document.scrape_queue_read.json
  }
}

resource "aws_lambda_function" "update_website" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["update_website"]
  handler          = "update_website.update_website"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.update_website.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
      "WEBSITE_TABLE_NAME" : data.aws_ssm_parameter.db_website_name.value,
    }
  }
}

resource "aws_iam_role" "update_website" {
  name                = local.lambda_names["update_website"]
  description         = "Allows Lambda to update website"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
  inline_policy {
    name   = "WriteToWebsiteDb"
    policy = data.aws_iam_policy_document.websites_db_put.json
  }
}

resource "aws_lambda_function" "options" {
  filename         = data.archive_file.handler.output_path
  function_name    = local.lambda_names["options"]
  handler          = "options.options"
  layers           = [aws_lambda_layer_version.layer.arn]
  role             = aws_iam_role.options.arn
  runtime          = "python3.9"
  timeout          = 10
  source_code_hash = data.archive_file.handler.output_base64sha256
  depends_on       = [aws_cloudwatch_log_group.all]
  environment {
    variables = {
      "ENVIRONMENT" : var.environment,
    }
  }
}

resource "aws_iam_role" "options" {
  name                = local.lambda_names["options"]
  description         = "Allows Lambda to be invoked"
  assume_role_policy  = data.aws_iam_policy_document.lambda_assume_role.json
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]
}
