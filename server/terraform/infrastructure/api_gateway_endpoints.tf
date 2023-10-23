# Order of creation is important
# method -> integration -> method response -> integration response

locals {
  # this determines when to redeploy API gateway
  all_integrations = [
    aws_api_gateway_method.create_website,
    aws_api_gateway_method.delete_website,
    aws_api_gateway_method.get_website,
    aws_api_gateway_method.get_websites,
    aws_api_gateway_method.get_scrape,
    aws_api_gateway_method.get_scrapes,
    aws_api_gateway_method.get_screenshot,
    aws_api_gateway_method.preview,
    aws_api_gateway_method.scrape_website,
    aws_api_gateway_method.scrape_websites,
    aws_api_gateway_method.scrape_website_options,
    aws_api_gateway_method.scrapes_options,
    aws_api_gateway_method.update_website,
    aws_api_gateway_method.websites_options,
    aws_api_gateway_method.website_options,
    aws_api_gateway_method.screenshot_options,

    aws_api_gateway_integration.create_website,
    aws_api_gateway_integration.delete_website,
    aws_api_gateway_integration.get_website,
    aws_api_gateway_integration.get_websites,
    aws_api_gateway_integration.get_scrape,
    aws_api_gateway_integration.get_scrapes,
    aws_api_gateway_integration.get_screenshot,
    aws_api_gateway_integration.preview,
    aws_api_gateway_integration.scrape_website,
    aws_api_gateway_integration.scrape_websites,
    aws_api_gateway_integration.scrape_website_options,
    aws_api_gateway_integration.scrapes_options,
    aws_api_gateway_integration.update_website,
    aws_api_gateway_integration.website_options,
    aws_api_gateway_integration.websites_options,
    aws_api_gateway_integration.screenshot_options,

    aws_api_gateway_method_response.create_website_200,
    aws_api_gateway_method_response.delete_website_200,
    aws_api_gateway_method_response.get_website_200,
    aws_api_gateway_method_response.get_websites_200,
    aws_api_gateway_method_response.get_scrape_200,
    aws_api_gateway_method_response.get_scrapes_200,
    aws_api_gateway_method_response.get_screenshot_200,
    aws_api_gateway_method_response.preview_200,
    aws_api_gateway_method_response.scrape_website_200,
    aws_api_gateway_method_response.scrape_website_options_200,
    aws_api_gateway_method_response.scrape_websites_200,
    aws_api_gateway_method_response.scrapes_options_200,
    aws_api_gateway_method_response.screenshot_options_200,
    aws_api_gateway_method_response.update_website_200,
    aws_api_gateway_method_response.website_options_200,
    aws_api_gateway_method_response.websites_options_200,

    aws_api_gateway_integration_response.website_options,
    aws_api_gateway_integration_response.websites_options,
    aws_api_gateway_integration_response.scrapes_options,
    aws_api_gateway_integration_response.scrape_website_options,
    aws_api_gateway_integration_response.screenshot_options,
  ]
}


// websites

resource "aws_api_gateway_resource" "websites" {
  path_part   = "websites"
  parent_id   = aws_api_gateway_rest_api.gateway.root_resource_id
  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_method" "get_websites" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.websites.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
}

resource "aws_api_gateway_integration" "get_websites" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.websites.id
  http_method             = aws_api_gateway_method.get_websites.http_method
  uri                     = aws_lambda_function.get_websites.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
}

resource "aws_api_gateway_method_response" "get_websites_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.websites.id
  http_method = aws_api_gateway_integration.get_websites.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = true
    "method.response.header.Access-Control-Allow-Methods"     = true
    "method.response.header.Access-Control-Allow-Origin"      = true
    "method.response.header.Access-Control-Allow-Credentials" = true
  }
}


resource "aws_api_gateway_method" "create_website" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.websites.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
}

resource "aws_api_gateway_integration" "create_website" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.websites.id
  http_method             = aws_api_gateway_method.create_website.http_method
  uri                     = aws_lambda_function.create_website.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
}

resource "aws_api_gateway_method_response" "create_website_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.websites.id
  http_method = aws_api_gateway_integration.create_website.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_method" "websites_options" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.websites.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "websites_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.websites.id
  http_method = aws_api_gateway_method.websites_options.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = <<EOF
        {
            "statusCode" : 200
        }
    EOF
  }
}

resource "aws_api_gateway_method_response" "websites_options_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.websites.id
  http_method = aws_api_gateway_integration.websites_options.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = true
    "method.response.header.Access-Control-Allow-Methods"     = true
    "method.response.header.Access-Control-Allow-Origin"      = true
    "method.response.header.Access-Control-Allow-Credentials" = true
  }
}

resource "aws_api_gateway_integration_response" "websites_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.websites.id
  http_method = aws_api_gateway_method_response.websites_options_200.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"      = "'${local.allowed_origins}'"
    "method.response.header.Access-Control-Allow-Credentials" = "'true'"
  }
}


// websites/{id}

resource "aws_api_gateway_resource" "website" {
  path_part   = "{website_id}"
  parent_id   = aws_api_gateway_resource.websites.id
  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_method" "get_website" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.website.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
  request_parameters = {
    "method.request.path.website_id" = true
  }
}

resource "aws_api_gateway_integration" "get_website" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.website.id
  http_method             = aws_api_gateway_method.get_website.http_method
  uri                     = aws_lambda_function.get_website.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  request_parameters = {
    "integration.request.path.website_id" : "method.request.path.website_id"
  }
}

resource "aws_api_gateway_method_response" "get_website_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.website.id
  http_method = aws_api_gateway_integration.get_website.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_method" "update_website" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.website.id
  http_method   = "PUT"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
  request_parameters = {
    "method.request.path.website_id" = true
  }
}

resource "aws_api_gateway_integration" "update_website" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.website.id
  http_method             = aws_api_gateway_method.update_website.http_method
  uri                     = aws_lambda_function.update_website.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  request_parameters = {
    "integration.request.path.website_id" : "method.request.path.website_id"
  }
}

resource "aws_api_gateway_method_response" "update_website_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.website.id
  http_method = aws_api_gateway_integration.update_website.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_method" "delete_website" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.website.id
  http_method   = "DELETE"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
  request_parameters = {
    "method.request.path.website_id" = true
  }
}

resource "aws_api_gateway_integration" "delete_website" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.website.id
  http_method             = aws_api_gateway_method.delete_website.http_method
  uri                     = aws_lambda_function.delete_website.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  request_parameters = {
    "integration.request.path.website_id" : "method.request.path.website_id"
  }
}

resource "aws_api_gateway_method_response" "delete_website_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.website.id
  http_method = aws_api_gateway_integration.delete_website.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_method" "website_options" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.website.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "website_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.website.id
  http_method = aws_api_gateway_method.website_options.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = <<EOF
        {
            "statusCode" : 200
        }
    EOF
  }
}

resource "aws_api_gateway_method_response" "website_options_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.website.id
  http_method = aws_api_gateway_integration.website_options.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "website_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.website.id
  http_method = aws_api_gateway_method_response.website_options_200.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,DELETE,PUT,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}


// websites/{id}/scrapes

resource "aws_api_gateway_resource" "scrapes" {
  path_part   = "scrapes"
  parent_id   = aws_api_gateway_resource.website.id
  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_method" "get_scrapes" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.scrapes.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
}

resource "aws_api_gateway_integration" "get_scrapes" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.scrapes.id
  http_method             = aws_api_gateway_method.get_scrapes.http_method
  uri                     = aws_lambda_function.get_scrapes.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
}

resource "aws_api_gateway_method_response" "get_scrapes_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrapes.id
  http_method = aws_api_gateway_integration.get_scrapes.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_method" "scrapes_options" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.scrapes.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "scrapes_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrapes.id
  http_method = aws_api_gateway_method.scrapes_options.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = <<EOF
        {
            "statusCode" : 200
        }
    EOF
  }
}

resource "aws_api_gateway_method_response" "scrapes_options_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrapes.id
  http_method = aws_api_gateway_integration.scrapes_options.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "scrapes_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrapes.id
  http_method = aws_api_gateway_method_response.scrapes_options_200.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}


// websites/{id}/scrapes/{id}

resource "aws_api_gateway_resource" "scrape" {
  path_part   = "{scrape_id}"
  parent_id   = aws_api_gateway_resource.scrapes.id
  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_method" "get_scrape" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.scrape.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
  request_parameters = {
    "method.request.path.scrape_id" = true
  }
}

resource "aws_api_gateway_integration" "get_scrape" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.scrape.id
  http_method             = aws_api_gateway_method.get_scrape.http_method
  uri                     = aws_lambda_function.get_scrape.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  request_parameters = {
    "integration.request.path.scrape_id" : "method.request.path.scrape_id"
  }
}

resource "aws_api_gateway_method_response" "get_scrape_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrape.id
  http_method = aws_api_gateway_integration.get_scrape.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}


// websites/{id}/scrapes/{id}/screenshot

resource "aws_api_gateway_resource" "screenshot" {
  path_part   = "screenshot"
  parent_id   = aws_api_gateway_resource.scrape.id
  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_method" "get_screenshot" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.screenshot.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
}

resource "aws_api_gateway_integration" "get_screenshot" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.screenshot.id
  http_method             = aws_api_gateway_method.get_screenshot.http_method
  uri                     = aws_lambda_function.get_screenshot.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
}

resource "aws_api_gateway_method_response" "get_screenshot_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.screenshot.id
  http_method = aws_api_gateway_integration.get_screenshot.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_method" "screenshot_options" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.screenshot.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "screenshot_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.screenshot.id
  http_method = aws_api_gateway_method.screenshot_options.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = <<EOF
        {
            "statusCode" : 200
        }
    EOF
  }
}

resource "aws_api_gateway_method_response" "screenshot_options_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.screenshot.id
  http_method = aws_api_gateway_integration.screenshot_options.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "screenshot_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.screenshot.id
  http_method = aws_api_gateway_method_response.screenshot_options_200.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}


// websites/preview

resource "aws_api_gateway_resource" "preview" {
  path_part   = "preview"
  parent_id   = aws_api_gateway_resource.websites.id
  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_method" "preview" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.preview.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
}

resource "aws_api_gateway_integration" "preview" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.preview.id
  http_method             = aws_api_gateway_method.preview.http_method
  uri                     = aws_lambda_function.preview.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
}

resource "aws_api_gateway_method_response" "preview_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.preview.id
  http_method = aws_api_gateway_integration.preview.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}


// websites/scrape

resource "aws_api_gateway_resource" "scrape_websites" {
  path_part   = "scrape"
  parent_id   = aws_api_gateway_resource.websites.id
  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_method" "scrape_websites" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.scrape_websites.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
}

resource "aws_api_gateway_integration" "scrape_websites" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.scrape_websites.id
  http_method             = aws_api_gateway_method.scrape_websites.http_method
  uri                     = aws_lambda_function.schedule_scrapes.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
}

resource "aws_api_gateway_method_response" "scrape_websites_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrape_websites.id
  http_method = aws_api_gateway_integration.scrape_websites.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}


// websites/{id}/scrape

resource "aws_api_gateway_resource" "scrape_website" {
  path_part   = "scrape"
  parent_id   = aws_api_gateway_resource.website.id
  rest_api_id = aws_api_gateway_rest_api.gateway.id
}

resource "aws_api_gateway_method" "scrape_website" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.scrape_website.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.gateway.id
}

resource "aws_api_gateway_integration" "scrape_website" {
  rest_api_id             = aws_api_gateway_rest_api.gateway.id
  resource_id             = aws_api_gateway_resource.scrape_website.id
  http_method             = aws_api_gateway_method.scrape_website.http_method
  uri                     = aws_lambda_function.scrape_website.invoke_arn
  content_handling        = "CONVERT_TO_TEXT"
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
}

resource "aws_api_gateway_method_response" "scrape_website_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrape_website.id
  http_method = aws_api_gateway_integration.scrape_website.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_method" "scrape_website_options" {
  rest_api_id   = aws_api_gateway_rest_api.gateway.id
  resource_id   = aws_api_gateway_resource.scrape_website.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "scrape_website_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrape_website.id
  http_method = aws_api_gateway_method.scrape_website_options.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = <<EOF
        {
            "statusCode" : 200
        }
    EOF
  }
}

resource "aws_api_gateway_method_response" "scrape_website_options_200" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrape_website.id
  http_method = aws_api_gateway_integration.scrape_website_options.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "scrape_website_options" {
  rest_api_id = aws_api_gateway_rest_api.gateway.id
  resource_id = aws_api_gateway_resource.scrape_website.id
  http_method = aws_api_gateway_method_response.scrape_website_options_200.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'"
    "method.response.header.Access-Control-Allow-Methods" = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

