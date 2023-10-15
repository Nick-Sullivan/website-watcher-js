import json
from typing import Dict

from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import GetScreenshotRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def get_screenshot(event, context=None):
    print(event)
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
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
        }}


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
    

if __name__ == '__main__':
    _get_screenshot({
        'user_id': 'user_id',
        'scrape_id': 'scrape_id'})
    