import os


def options(event, context=None):
    request_origin = event['headers']['origin']
    response_origin = get_response_origin(request_origin)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Origin': response_origin,
            'Access-Control-Allow-Methods': 'GET,OPTIONS',
            'Access-Control-Allow-Credentials': 'true',
        }
    }

def get_response_origin(requested_origin):
    env = os.environ['ENVIRONMENT'].lower()
    if env == 'prod':
        return 'http://websitewatcherjs-prod.com.s3-website-ap-southeast-2.amazonaws.com'

    if requested_origin.startswith('http://localhost:'):
        return requested_origin
    else:
        return f'http://websitewatcherjs-{env}.com.s3-website-ap-southeast-2.amazonaws.com'
    