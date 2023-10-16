
import pytest

from .endpoints import (
    create_website,
    delete_website,
    get_websites,
    update_website,
)


@pytest.fixture(scope='module')
def setup():
    create_req = {'name': 'website_one', 'url': 'https://google.com'}
    create_res = create_website(create_req)
    website_id = create_res.json()['website_id']
    try:
        yield {'website_id': website_id}
    finally:
        delete_req = {'website_id': website_id}
        delete_website(delete_req)


@pytest.fixture(scope='module')
def response(setup):
    update_req = {
        'website_id': setup['website_id'],
        'name': 'NewName',
        'url': 'NewUrl',
        'frequency': 'WEEKLY'}
    update_res = update_website(update_req)
    yield update_res


@pytest.fixture(scope='module')
def response_body(response):
    yield response.json()


@pytest.fixture(scope='module')
def get_websites_response_body(setup, response):
    response = get_websites().json()
    matching = [
        w for w in response['websites']
        if w['website_id'] == setup['website_id']]
    yield matching


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_didnt_create_a_new_website(get_websites_response_body):
    assert len(get_websites_response_body) == 1


def test_it_updated_the_name(get_websites_response_body):
    assert get_websites_response_body[0]['name'] == 'NewName'


def test_it_updated_the_url(get_websites_response_body):
    assert get_websites_response_body[0]['url'] == 'NewUrl'


def test_it_updated_the_frequency(get_websites_response_body):
    assert get_websites_response_body[0]['frequency'] == 'WEEKLY'
    