import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.domain import timestamp
from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import GetScrapeRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def get_scrape(event, context=None):
    print(event)

    request_origin = event.get('headers', {}).get('origin')
    headers = get_response_headers(request_origin)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = {
        'user_id': cognito_id,
        'website_id': event['pathParameters']['website_id'],
        'scrape_id': event['pathParameters']['scrape_id']}

    try:
        response = _get_scrape(body)
    except LogicalException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': str(e)})}

    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': headers}


def _get_scrape(request_body: Dict):
    
    error_msgs = validate_request(request_body, GetScrapeRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = GetScrapeRequest(**request_body)
    
    scrape = scrape_service.get_scrape(request)

    return {
        'user_id': scrape.user_id,
        'website_id': scrape.website_id,
        'scrape_id': scrape.scrape_id,
        'scraped_at': timestamp(scrape.scraped_at)}
