import json

import pytest
from domain_models.domain import Frequency, Website, create_unique_key
from handler.get_website import get_website
from infrastructure import website_store


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    website_store.create(Website(user_id=user_id, website_id='1', name='One', url='https://one.com', frequency=Frequency.DAILY))
    try:
        yield {'user_id': user_id, 'website_id': '1'}
    finally:
        website_store.delete(user_id, '1')


@pytest.fixture(scope='module')
def response(setup):
    request = {'user_id': setup['user_id']}
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    yield get_website({
        'body': json.dumps(request),
        'pathParameters': {'website_id': setup['website_id']},
        'requestContext': context})


@pytest.fixture
def response_body(response):
    yield json.loads(response['body'])


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_returns_name(response_body):
    assert 'name' in response_body


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body


def test_it_returns_website_id(response_body):
    assert 'website_id' in response_body


def test_it_returns_url(response_body):
    assert 'url' in response_body


def test_it_returns_frequency(response_body):
    assert 'frequency' in response_body