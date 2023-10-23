import os

from api_layer.response_service import get_response_headers


def test_it_allows_localhost_in_lower_environments():
    os.environ['ENVIRONMENT'] = 'dev'
    headers = get_response_headers('http://localhost:3000')
    assert headers['Access-Control-Allow-Origin'] == 'http://localhost:3000'


def test_it_blocks_localhost_in_production_environment():
    os.environ['ENVIRONMENT'] = 'prod'
    headers = get_response_headers('http://localhost:3000')
    assert headers['Access-Control-Allow-Origin'] != 'http://localhost:3000'


def test_it_returns_empty_if_no_origin_is_supplied():
    os.environ['ENVIRONMENT'] = 'dev'
    headers = get_response_headers(None)
    assert headers['Access-Control-Allow-Origin'] == ''
