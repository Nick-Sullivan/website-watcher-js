import json

import pytest
from domain_models.domain import Frequency, create_unique_key
from handler.create_website import create_website
from infrastructure import website_store


@pytest.fixture(scope='module')
def response():
    user_id = create_unique_key()
    request = {'user_id': user_id, 'name': 'website_one', 'url': 'https://google.com'}
    context = {'authorizer': {'claims': {'cognito:username': user_id}}}
    yield create_website({'body': json.dumps(request), 'requestContext': context})


@pytest.fixture(scope='module')
def response_body(response):
    body = json.loads(response['body'])
    try:
        yield body
    finally:
        website_store.delete(body['user_id'], body['website_id'])


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body


def test_it_returns_website_id(response_body):
    assert 'website_id' in response_body


def test_it_saves_website_in_db(response_body):
    website = website_store.get(
        user_id=response_body['user_id'],
        website_id=response_body['website_id'])
    assert website is not None


def test_it_defaults_to_daily_frequency(response_body):
    website = website_store.get(
        user_id=response_body['user_id'],
        website_id=response_body['website_id'])
    assert website.frequency == Frequency.DAILY
