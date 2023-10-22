# Database to hold website/watcher registrations

resource "aws_dynamodb_table" "websites" {
  name         = "${local.prefix}-Websites"
  hash_key     = "user_id"
  range_key    = "website_id"
  billing_mode = "PAY_PER_REQUEST"
  attribute {
    name = "user_id"
    type = "S"
  }
  attribute {
    name = "website_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "scrape" {
  name         = "${local.prefix}-Scrapes"
  hash_key     = "partition_key"
  range_key    = "scrape_id"
  billing_mode = "PAY_PER_REQUEST"
  attribute {
    name = "partition_key"
    type = "S"
  }
  attribute {
    name = "scrape_id"
    type = "S"
  }
}
