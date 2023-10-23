import json
from typing import Dict

from api_layer.response_service import get_response_headers
from domain_models.requests import ScheduleScrapeRequest
from domain_models.validation import validate_request
from domain_services import schedule_service


def schedule_scrapes(event, context=None):
    print(event)


    if is_invoked_from_eventbridge(event):
        print('Invoked from EventBridge')
        return _schedule_scrapes({'user_id': 'a0e71016-244b-4a11-b2e4-4026d562e4a0'})
    else:
        print('Invoked from API Gateway')
        cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
        body = json.loads(event['body'])
        body['user_id'] = cognito_id
        return _schedule_scrapes(body, event.get('headers', {}))


def _schedule_scrapes(request_body: Dict, request_headers: Dict):
    
    request_body = _fill_defaults(request_body)
    request_origin = request_headers.get('origin')
    headers = get_response_headers(request_origin)

    error_msgs = validate_request(request_body, ScheduleScrapeRequest)
    if error_msgs:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': error_msgs})}

    request = ScheduleScrapeRequest(**request_body)
    
    websites = schedule_service.schedule_scrapes(request)

    response = {
        'websites': [{
            'user_id': w.user_id,
            'website_id': w.website_id,
            'name': w.name,
            'url': w.url}
        for w in websites]}
    
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': headers}


def is_invoked_from_eventbridge(event) -> bool:
    return event.get('source') == 'aws.events'


def _fill_defaults(request_body) -> Dict:
    if 'ignore_frequency' not in request_body:
        request_body['ignore_frequency'] = False
    return request_body
