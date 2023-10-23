from api_layer.response_service import get_response_headers


def options(event, context=None):
    request_origin = event.get('headers', {}).get('origin')

    headers = get_response_headers(request_origin)

    return {
        'statusCode': 200,
        'headers': headers
    }
    