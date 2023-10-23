import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import GetScreenshotRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def get_screenshot(event, context=None):
    print(event)

    request_origin = event.get('headers', {}).get('origin')
    headers = get_response_headers(request_origin)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = {
        'user_id': cognito_id,
        'website_id': event['pathParameters']['website_id'],
        'scrape_id': event['pathParameters']['scrape_id']}
    
    try:
        response = _get_screenshot(body)
    except LogicalException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': str(e)})}

    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': headers}


def _get_screenshot(request_body: Dict):
    
    error_msgs = validate_request(request_body, GetScreenshotRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = GetScreenshotRequest(**request_body)
    
    url = scrape_service.get_screenshot(request)

    return {
        'user_id': request.user_id,
        'scrape_id': request.scrape_id,
        'screenshot_url': url}
    