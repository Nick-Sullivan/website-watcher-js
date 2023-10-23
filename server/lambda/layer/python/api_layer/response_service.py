import os


def get_response_headers(request_origin):
    response_origin = _get_response_origin(request_origin)

    return {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Origin': response_origin,
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Credentials': 'true',
    }


def _get_response_origin(requested_origin):
    env = os.environ.get('ENVIRONMENT', '').lower()
    if env == 'prod':
        return 'http://websitewatcherjs-prod.com.s3-website-ap-southeast-2.amazonaws.com'

    if requested_origin is None:
        return ''

    if requested_origin.startswith('http://localhost:'):
        return requested_origin
        
    return f'http://websitewatcherjs-{env}.com.s3-website-ap-southeast-2.amazonaws.com'
    