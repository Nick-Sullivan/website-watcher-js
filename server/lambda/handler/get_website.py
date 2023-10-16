import json
from typing import Dict

from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import GetWebsiteRequest
from domain_models.validation import validate_request
from domain_services import website_service


def get_website(event, context=None):
    print(event)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = {
        'user_id': cognito_id,
        'website_id': event['pathParameters']['website_id']}
            
    try:
        response = _get_website(body)
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

def _get_website(request_body: Dict) -> Dict:
    error_msgs = validate_request(request_body, GetWebsiteRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = GetWebsiteRequest(**request_body)
    
    website = website_service.get_website(request)

    return {
        'user_id': website.user_id,
        'website_id': website.website_id,
        'name': website.name,
        'url': website.url,
        'frequency': website.frequency.value}
