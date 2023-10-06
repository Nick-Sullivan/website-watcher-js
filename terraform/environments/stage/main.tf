terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.48.0"
    }
  }
  backend "s3" {
    bucket = "nicks-terraform-states"
    key    = "website_watcher_js/stage/terraform.tfstate"
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
  domain       = "websitewatcherjs.com"
  root_dir     = "${path.root}/../../.."
  website_dir  = "${local.root_dir}/website"

  tags = {
    Project = "Website Watcher JS"
  }
}


# S3 bucket for hosting the website

resource "aws_s3_bucket" "website" {
  bucket = local.domain
}

resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.bucket
  index_document {
    suffix = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "website" {
  bucket = aws_s3_bucket.website.id
}

resource "aws_s3_bucket_policy" "website" {
  bucket = aws_s3_bucket.website.id
  policy = data.aws_iam_policy_document.allow_public_get.json
}

data "aws_iam_policy_document" "allow_public_get" {
  statement {
    actions = [
      "s3:GetObject"
    ]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.website.id}/*"
    ]
    sid = "PublicReadGetObject"
  }
}

resource "aws_s3_bucket_metric" "website" {
  bucket = aws_s3_bucket.website.bucket
  name   = local.prefix
}

# Contents of the website


data "archive_file" "website" {
  type        = "zip"
  source_dir  = local.website_dir
  output_path = "${local.root_dir}/website.zip"
  excludes    = [".next", "out"]
}

resource "terraform_data" "build" {
  triggers_replace = [
    data.archive_file.website.output_base64sha256
  ]
  provisioner "local-exec" {
    working_dir = local.website_dir
    command     = "npm run build"
  }
}
