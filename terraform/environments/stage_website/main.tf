terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.48.0"
    }
  }
  backend "s3" {
    bucket = "nicks-terraform-states"
    key    = "website_watcher_js/stage_website/terraform.tfstate"
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
  domain       = "websitewatcherjs.com"
  root_dir     = "${path.root}/../../.."
  website_dir  = "${local.root_dir}/website"

  tags = {
    Project = "Website Watcher JS"
  }
}



module "template_files" {
  # Calculates the content_type of each file.
  # https://registry.terraform.io/modules/hashicorp/dir/template/latest
  source   = "hashicorp/dir/template"
  base_dir = "${local.website_dir}/out"
}

resource "aws_s3_object" "static_files" {
  for_each     = module.template_files.files
  bucket       = local.domain
  key          = each.key
  content_type = each.value.content_type
  source       = each.value.source_path
  content      = each.value.content
  etag         = each.value.digests.md5
}