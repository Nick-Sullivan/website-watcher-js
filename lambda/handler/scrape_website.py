import json
from typing import Dict

from domain_models.requests import ScrapeWebsiteRequest
from domain_models.validation import validate_request
from domain_services import scrape_service


def scrape_website(event, context=None):
    print(event)

    if is_invoked_from_sqs(event):
        print('Invoked from SQS')
        assert len(event['Records']) == 1
        event = event['Records'][0]
        body = json.loads(event['body'])
    else:
        print('Invoked from API Gateway')
        cognito_id = event['requestContext']['authorizer']['claims']['cognito:username']
        body = {
            'user_id': cognito_id,
            'website_id': event['pathParameters']['website_id']}

    return _scrape_website(body)


def _scrape_website(request_body: Dict):
    
    error_msgs = validate_request(request_body, ScrapeWebsiteRequest)
    if error_msgs:
        return {
            'statusCode': 400,
            'body': json.dumps({'errors': error_msgs})}

    request = ScrapeWebsiteRequest(**request_body)
    
    scrape = scrape_service.scrape_website(request)

    response = {
        'user_id': scrape.user_id,
        'scrape_id': scrape.scrape_id,
        'website_id': scrape.website_id}
    
    return {
        'statusCode': 200,
        'body': json.dumps(response),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST',
        }}


def is_invoked_from_sqs(event):
    return 'Records' in event

    
if __name__ == '__main__':
    _scrape_website({
        'user_id': 'test',
        'website_id': 'ebc2470e-4c5d-4a4e-bc1e-b85c7fb70f53'})