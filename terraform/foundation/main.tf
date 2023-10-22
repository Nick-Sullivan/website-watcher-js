terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.48.0"
    }
  }
  # Key is dynamic, provided by the makefile
  backend "s3" {
    bucket = "nicks-terraform-states"
    region = "ap-southeast-2"
  }
}

provider "aws" {
  region = "ap-southeast-2"
  default_tags {
    tags = local.tags
  }
}

data "aws_caller_identity" "identity" {}

locals {
  prefix                    = "WebsiteWatcherJs-${title(var.environment)}"
  prefix_lower              = "website-watcher-js-${lower(var.environment)}"
  prefix_parameter          = "/WebsiteWatcherJs/${title(var.environment)}"
  aws_account_id            = data.aws_caller_identity.identity.account_id
  root_dir                  = "${path.root}/../.."
  website_dir               = "${local.root_dir}/client"
  lambda_dir                = "${local.root_dir}/server/lambda"
  automated_tester_username = "nick.dave.sullivan+1@gmail.com"

  tags = {
    Project     = "Website Watcher JS"
    Environment = var.environment
  }
}
