terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.48.0"
    }
  }
  backend "s3" {
    bucket = "nicks-terraform-states"
    key    = "website_watcher_js/stage/infrastructure/terraform.tfstate"
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
  prefix                    = "WebsiteWatcherJs"
  prefix_lower              = "website-watcher-js"
  domain                    = "websitewatcherjs.com"
  aws_account_id            = data.aws_caller_identity.identity.account_id
  automated_tester_username = "nick.dave.sullivan+testing@gmail.com"
  root_dir                  = "${path.root}/../../../.."
  website_dir               = "${local.root_dir}/client"
  server_dir                = "${local.root_dir}/server"
  bruno_dir                 = "${local.server_dir}/bruno"
  lambda_dir                = "${local.server_dir}/lambda"
  foundation_output         = jsondecode(file("../foundation/output.json"))

  lambda_names = {
    "create_website"   = "${local.prefix}-CreateWebsite"
    "delete_website"   = "${local.prefix}-DeleteWebsite"
    "get_website"      = "${local.prefix}-GetWebsite"
    "get_websites"     = "${local.prefix}-GetWebsites"
    "get_scrape"       = "${local.prefix}-GetScrape"
    "get_scrapes"      = "${local.prefix}-GetScrapes"
    "get_screenshot"   = "${local.prefix}-GetScreenshot"
    "preview"          = "${local.prefix}-Preview"
    "schedule_scrapes" = "${local.prefix}-ScheduleScrapes"
    "scrape_website"   = "${local.prefix}-ScrapeWebsite"
    "update_website"   = "${local.prefix}-UpdateWebsite"
  }

  tags = {
    Project = "Website Watcher JS Stage"
  }
}
