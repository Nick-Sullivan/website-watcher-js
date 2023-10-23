import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.domain import Frequency
from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import CreateWebsiteRequest
from domain_models.validation import validate_request
from domain_services import website_service


def create_website(event, context=None):
    print(event)

    request_origin = event.get('headers', {}).get('origin')
    headers = get_response_headers(request_origin)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = json.loads(event['body'])
    body['user_id'] = cognito_id

    try:
        response = _create_website(body)
        
    except LogicalException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': str(e)})}

    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': headers}

        
def _create_website(request_body: Dict) -> Dict:

    request_body = _fill_defaults(request_body)
    
    error_msgs = validate_request(request_body, CreateWebsiteRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request_body = _populate_enums(request_body)
    
    request = CreateWebsiteRequest(**request_body)
    
    website_id = website_service.create_website(request)

    return {
        'user_id': request.user_id,
        'website_id': website_id}


def _fill_defaults(request_body) -> Dict:
    if 'frequency' not in request_body:
        request_body['frequency'] = Frequency.DAILY.value
    return request_body


def _populate_enums(request_body) -> Dict:
    request_body['frequency'] = Frequency(request_body['frequency'])
    return request_body
