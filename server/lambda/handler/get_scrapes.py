import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.domain import timestamp
from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import GetScrapesRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def get_scrapes(event, context=None):
    print(event)

    request_origin = event.get('headers', {}).get('origin')
    headers = get_response_headers(request_origin)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = {
        'user_id': cognito_id,
        'website_id': event['pathParameters']['website_id']}

    try:
        response = _get_scrapes(body)
    except LogicalException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': str(e)})}

    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': headers}


def _get_scrapes(request_body: Dict):
    
    error_msgs = validate_request(request_body, GetScrapesRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = GetScrapesRequest(**request_body)
    
    scrapes = scrape_service.get_scrapes(request)

    return {
        'scrapes': [{
            'user_id': s.user_id,
            'website_id': s.website_id,
            'scrape_id': s.scrape_id,
            'scraped_at': timestamp(s.scraped_at)}
        for s in scrapes]}
    