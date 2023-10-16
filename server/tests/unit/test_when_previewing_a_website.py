import json

import pytest
from domain_models.domain import create_unique_key
from handler.preview import preview
from infrastructure import screenshot_store


@pytest.fixture(scope='module')
def response():
    user_id = create_unique_key()
    request = {'user_id': user_id, 'url': 'https://nicksurl.com'}
    context = {'authorizer': {'claims': {'cognito:username': user_id}}}
    yield preview({'body': json.dumps(request), 'requestContext': context})


@pytest.fixture
def response_body(response):
    yield json.loads(response['body'])


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body


def test_it_returns_a_url(response_body):
    assert 'screenshot_url' in response_body
