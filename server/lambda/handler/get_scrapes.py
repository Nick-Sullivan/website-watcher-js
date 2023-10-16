import json
from typing import Dict

from domain_models.domain import timestamp
from domain_models.exceptions import InvalidRequestException, LogicalException
from domain_models.requests import GetScrapesRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def get_scrapes(event, context=None):
    print(event)

    cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
    body = {
        'user_id': cognito_id,
        'website_id': event['pathParameters']['website_id']}

    try:
        response = _get_scrapes(body)
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


def _get_scrapes(request_body: Dict):
    
    error_msgs = validate_request(request_body, GetScrapesRequest)
    if error_msgs:
        raise InvalidRequestException(json.dumps({'errors': error_msgs}))

    request = GetScrapesRequest(**request_body)
    
    scrapes = scrape_service.get_scrapes(request)

    return {
        'scrapes': [{
            'user_id': s.user_id,
            'website_id': s.website_id,
            'scrape_id': s.scrape_id,
            'scraped_at': timestamp(s.scraped_at)}
        for s in scrapes]}
    

if __name__ == '__main__':
    _get_scrapes({
        'user_id': 'a0e71016-244b-4a11-b2e4-4026d562e4a0',
        'website_id': 'ebc2470e-4c5d-4a4e-bc1e-b85c7fb70f53'})