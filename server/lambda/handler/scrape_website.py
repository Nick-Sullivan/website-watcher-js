import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.requests import ScrapeWebsiteRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def scrape_website(event, context=None):
    print(event)

    if is_invoked_from_sqs(event):
        print('Invoked from SQS')
        assert len(event['Records']) == 1
        event = event['Records'][0]
        body = json.loads(event['body'])
        headers = {}
    else:
        print('Invoked from API Gateway')
        cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
        body = {
            'user_id': cognito_id,
            'website_id': event['pathParameters']['website_id']}
        headers = event.get('headers', {})

    return _scrape_website(body, headers)


def _scrape_website(request_body: Dict, request_headers: Dict):
    
    request_origin = request_headers.get('origin')
    headers = get_response_headers(request_origin)

    error_msgs = validate_request(request_body, ScrapeWebsiteRequest)
    if error_msgs:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': error_msgs})}

    request = ScrapeWebsiteRequest(**request_body)
    
    scrape = scrape_service.scrape_website(request)

    response = {
        'user_id': scrape.user_id,
        'scrape_id': scrape.scrape_id,
        'website_id': scrape.website_id}
    
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': headers}


def is_invoked_from_sqs(event):
    return 'Records' in event
