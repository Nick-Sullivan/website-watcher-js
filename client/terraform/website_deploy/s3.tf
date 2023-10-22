

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
  depends_on = [aws_s3_bucket_public_access_block.website]
  bucket     = aws_s3_bucket.website.id
  policy     = data.aws_iam_policy_document.allow_public_get.json
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

module "template_files" {
  # Calculates the content_type of each file.
  # https://registry.terraform.io/modules/hashicorp/dir/template/latest
  depends_on = [aws_s3_bucket.website]
  source     = "hashicorp/dir/template"
  base_dir   = "${local.root_dir}/out"
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
