import json
from typing import Dict

from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import GetWebsitesRequest
from domain_models.validation import validate_request
from domain_services import website_service


def get_websites(event, context=None):
    print(event)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = {'user_id': cognito_id}

    try:
        response = _get_websites(body)
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
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Credentials': 'true',
        }}


def _get_websites(request_body: Dict):
    error_msgs = validate_request(request_body, GetWebsitesRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = GetWebsitesRequest(**request_body)
    
    websites = website_service.get_websites(request)

    return {
        'websites': [{
            'user_id': w.user_id,
            'website_id': w.website_id,
            'name': w.name,
            'url': w.url,
            'frequency': w.frequency.value}
        for w in websites]}
        