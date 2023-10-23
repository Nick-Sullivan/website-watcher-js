import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import DeleteWebsiteRequest
from domain_models.validation import validate_request
from domain_services import website_service


def delete_website(event, context=None):
    print(event)

    request_origin = event.get('headers', {}).get('origin')
    headers = get_response_headers(request_origin)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = {
        'user_id': cognito_id,
        'website_id': event['pathParameters']['website_id']}

    try:
        _delete_website(body)
    except LogicalException as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': str(e)})}

    return {
        'statusCode': 200,
        'headers': headers}


def _delete_website(request_body: Dict):
    
    error_msgs = validate_request(request_body, DeleteWebsiteRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = DeleteWebsiteRequest(**request_body)
    
    website_service.delete_website(request)
    