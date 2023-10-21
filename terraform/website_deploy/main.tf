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

locals {
  prefix           = "WebsiteWatcherJs-${var.environment}"
  prefix_parameter = "/WebsiteWatcherJs/${title(var.environment)}"
  domain           = "websitewatcherjs-${lower(var.environment)}.com"
  root_dir         = "${path.root}/../.."
  website_dir      = "${local.root_dir}/client"

  tags = {
    Project     = "Website Watcher JS"
    Environment = var.environment
  }
}
