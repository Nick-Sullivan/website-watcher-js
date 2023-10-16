import json
from typing import Dict

from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import PreviewWebsiteRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def preview(event, context=None):
    print(event)
    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = json.loads(event['body'])
    body['user_id'] = cognito_id

    try:
        response = _preview(body)
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
            'Access-Control-Allow-Methods': 'POST,OPTIONS',
        }}


def _preview(request_body: Dict) -> Dict:
    
    error_msgs = validate_request(request_body, PreviewWebsiteRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = PreviewWebsiteRequest(**request_body)
    
    screenshot_url = scrape_service.preview(request)

    return {
        'user_id': request.user_id,
        'screenshot_url': screenshot_url}


if __name__ == '__main__':
    response = _preview({
        'user_id': 'user_id',
        'url': 'https://google.com'})