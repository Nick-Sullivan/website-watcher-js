import json

import pytest
from domain_models.domain import Frequency, Website, create_unique_key
from handler.get_websites import get_websites
from infrastructure import website_store


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    other_user_id = create_unique_key()
    website_store.create(Website(user_id=user_id, website_id='1', name='One', url='https://one.com', frequency=Frequency.DAILY))
    website_store.create(Website(user_id=user_id, website_id='2', name='Two', url='https://two.com', frequency=Frequency.DAILY))
    website_store.create(Website(user_id=other_user_id, website_id='3', name='Three', url='https://three.com', frequency=Frequency.DAILY))
    try:
        yield {'user_id': user_id}
    finally:
        website_store.delete(user_id, '1')
        website_store.delete(user_id, '2')
        website_store.delete(other_user_id, '3')


@pytest.fixture(scope='module')
def response(setup):
    request = {'user_id': setup['user_id']}
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    yield get_websites({'body': json.dumps(request), 'requestContext': context})


@pytest.fixture
def response_body(response):
    yield json.loads(response['body'])


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_returns_websites_for_this_user(response_body):
    assert 'websites' in response_body
    assert len(response_body['websites']) == 2
    assert response_body['websites'][0]['name'] == 'One'
    assert response_body['websites'][1]['name'] == 'Two'


def test_it_returns_name(response_body):
    assert 'name' in response_body['websites'][0]


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body['websites'][0]


def test_it_returns_website_id(response_body):
    assert 'website_id' in response_body['websites'][0]


def test_it_returns_url(response_body):
    assert 'url' in response_body['websites'][0]


def test_it_returns_frequency(response_body):
    assert 'frequency' in response_body['websites'][0]