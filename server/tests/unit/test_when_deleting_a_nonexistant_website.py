import json

import pytest
from domain_models.domain import create_unique_key
from handler.delete_website import delete_website


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    yield {'user_id': user_id, 'website_id': 'wid'}


@pytest.fixture(scope='module')
def response(setup):
    request = {'user_id': setup['user_id']}
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    yield delete_website({
        'body': json.dumps(request),
        'requestContext': context,
        'pathParameters': {'website_id': setup['website_id']}})


def test_it_returns_status_400(response):
    assert response['statusCode'] == 400


def test_it_gives_helpful_error_message(setup, response):
    website_id = setup['website_id']
    body = json.loads(response['body'])
    assert body['errors'] == f'Unable to find website with ID {website_id}'
