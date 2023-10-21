
# S3 bucket for saving screenshots

resource "aws_s3_bucket" "watch_results" {
  bucket = local.prefix_lower
}

resource "aws_s3_bucket_metric" "watch_results" {
  bucket = aws_s3_bucket.watch_results.bucket
  name   = local.prefix
}

resource "aws_s3_bucket_lifecycle_configuration" "watch_results" {
  bucket = aws_s3_bucket.watch_results.bucket
  rule {
    id     = "remove-temp-screenshots"
    status = "Enabled"
    filter {
      prefix = "temp/"
    }
    expiration {
      days = 1
    }
  }
}
