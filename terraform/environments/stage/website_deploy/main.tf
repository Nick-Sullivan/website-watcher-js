terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.48.0"
    }
  }
  backend "s3" {
    bucket = "nicks-terraform-states"
    key    = "website_watcher_js/stage/website_deploy/terraform.tfstate"
    region = "ap-southeast-2"
  }
}

provider "aws" {
  region = "ap-southeast-2"
  default_tags {
    tags = local.tags
  }
}

locals {
  prefix       = "WebsiteWatcherJs"
  prefix_lower = "website-watcher-js"
  prefix_upper = "WEBSITE_WATCHER_JS"
  domain       = "websitewatcherjs.com"
  root_dir     = "${path.root}/../../../.."
  website_dir  = "${local.root_dir}/client"

  tags = {
    Project = "Website Watcher JS Stage"
  }
}
