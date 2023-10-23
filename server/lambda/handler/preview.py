import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import PreviewWebsiteRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def preview(event, context=None):
    print(event)

    request_origin = event.get('headers', {}).get('origin')
    headers = get_response_headers(request_origin)

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
        'headers': headers}


def _preview(request_body: Dict) -> Dict:
    
    error_msgs = validate_request(request_body, PreviewWebsiteRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = PreviewWebsiteRequest(**request_body)
    
    screenshot_url = scrape_service.preview(request)

    return {
        'user_id': request.user_id,
        'screenshot_url': screenshot_url}
