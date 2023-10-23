import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.domain import Frequency
from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import UpdateWebsiteRequest
from domain_models.validation import validate_request
from domain_services import website_service


def update_website(event, context=None):
    print(event)
    request_origin = event.get('headers', {}).get('origin')
    headers = get_response_headers(request_origin)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = json.loads(event['body'])
    body['user_id'] = cognito_id
    try:
        if event['pathParameters']['website_id'] != body['website_id']:
            raise InvalidRequestException('ID in URL does not match ID in body')

        _update_website(body)

    except LogicalException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': str(e)})}

    return {
        'statusCode': 200,
        'headers': headers}

def _update_website(request_body: Dict) -> Dict:
    
    error_msgs = validate_request(request_body, UpdateWebsiteRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request_body = _populate_enums(request_body)

    request = UpdateWebsiteRequest(**request_body)
    
    website_service.update_website(request)
    

def _populate_enums(request_body) -> Dict:
    request_body['frequency'] = Frequency(request_body['frequency'])
    return request_body
    