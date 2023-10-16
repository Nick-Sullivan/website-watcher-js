import json

import pytest
from domain_models.domain import Frequency, Website, create_unique_key
from handler.update_website import update_website
from infrastructure import website_store


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    website = Website(user_id=user_id, website_id='wid', name='One', url='https://one.com', frequency=Frequency.DAILY)
    website_store.create(website)
    try:
        yield {'user_id': user_id, 'website_id': 'wid'}
    finally:
        website_store.delete(user_id, 'wid')


@pytest.fixture(scope='module')
def response(setup):
    request = {
        'user_id': setup['user_id'],
        'website_id': setup['website_id'],
        'name': 'NewName',
        'url': 'NewUrl',
        'frequency': 'WEEKLY'}
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    yield update_website({
        'body': json.dumps(request),
        'requestContext': context,
        'pathParameters': {'website_id': setup['website_id']}})


@pytest.fixture(scope='module')
def response_body(response):
    yield json.loads(response['body'])


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_updates_website_in_db(setup, response):
    website = website_store.get(
        user_id=setup['user_id'],
        website_id=setup['website_id'])
    assert website.name == 'NewName'
    assert website.url == 'NewUrl'
    assert website.frequency == Frequency.WEEKLY
