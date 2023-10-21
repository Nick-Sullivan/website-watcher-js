data "aws_caller_identity" "identity" {}


data "aws_ssm_parameter" "cognito_client_id" {
  name = "${local.prefix_parameter}/Cognito/ClientId"
}

data "aws_ssm_parameter" "cognito_user_pool_arn" {
  name = "${local.prefix_parameter}/Cognito/UserPool/Arn"
}

data "aws_ssm_parameter" "cognito_user_pool_id" {
  name = "${local.prefix_parameter}/Cognito/UserPool/Id"
}

data "aws_ssm_parameter" "db_scrape_arn" {
  name = "${local.prefix_parameter}/Db/Scrape/Arn"
}

data "aws_ssm_parameter" "db_scrape_name" {
  name = "${local.prefix_parameter}/Db/Scrape/Name"
}

data "aws_ssm_parameter" "db_website_arn" {
  name = "${local.prefix_parameter}/Db/Website/Arn"
}

data "aws_ssm_parameter" "db_website_name" {
  name = "${local.prefix_parameter}/Db/Website/Name"
}

data "aws_ssm_parameter" "ecr_name" {
  name = "${local.prefix_parameter}/Ecr/Name"
}

data "aws_ssm_parameter" "ecr_url" {
  name = "${local.prefix_parameter}/Ecr/Url"
}

data "aws_ssm_parameter" "s3_name" {
  name = "${local.prefix_parameter}/S3/Name"
}

data "aws_ssm_parameter" "s3_snapshot_arn" {
  name = "${local.prefix_parameter}/S3/Snapshot/Arn"
}

data "aws_ssm_parameter" "s3_snapshot_name" {
  name = "${local.prefix_parameter}/S3/Snapshot/Name"
}
