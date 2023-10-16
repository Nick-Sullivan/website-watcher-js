
import pytest

from .endpoints import create_website, delete_website, get_screenshot, scrape_website


@pytest.fixture(scope='module')
def setup():

    create_req = {'name': 'website_one', 'url': 'https://google.com'}
    create_res = create_website(create_req)
    website_id = create_res.json()['website_id']

    scrape_req = {'website_id': website_id}
    scrape_res = scrape_website(scrape_req)
    scrape_id = scrape_res.json()['scrape_id']

    try:
        yield {'website_id': website_id, 'scrape_id': scrape_id}
    finally:
        delete_req = {'website_id': website_id}
        delete_website(delete_req)


@pytest.fixture(scope='module')
def response(setup):
    screenshot_req = {'website_id': setup['website_id'], 'scrape_id': setup['scrape_id']}
    yield get_screenshot(screenshot_req)


@pytest.fixture(scope='module')
def response_body(response):
    yield response.json()


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_returns_screenshot_url(response_body):
    assert 'screenshot_url' in response_body
