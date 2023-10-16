import json

import pytest
from domain_models.domain import Frequency, Scrape, Website, create_unique_key, now
from domain_models.exceptions import (
    ScrapeNotFoundException,
    ScreenshotNotFoundException,
    WebsiteNotFoundException,
)
from handler.delete_website import delete_website
from infrastructure import scrape_store, screenshot_store, website_store


@pytest.fixture(scope='module')
def setup():
    user_id = create_unique_key()
    scrape = Scrape(user_id=user_id, website_id='wid', scrape_id='sid', scraped_at=now())
    website = Website(user_id=user_id, website_id='wid', name='One', url='https://one.com', frequency=Frequency.DAILY)
    website_store.create(website)
    scrape_store.create(scrape)
    screenshot_store.save(scrape, screenshot='screenshot')
    yield {'user_id': user_id, 'website_id': 'wid', 'scrape_id': 'sid', 'scrape': scrape}


@pytest.fixture(scope='module')
def response(setup):
    request = {'user_id': setup['user_id']}
    context = {'authorizer': {'claims': {'cognito:username': setup['user_id']}}}
    yield delete_website({
        'body': json.dumps(request),
        'requestContext': context,
        'pathParameters': {'website_id': setup['website_id']}})


def test_it_returns_status_200(response):
    assert response['statusCode'] == 200


def test_it_deletes_website_in_db(setup, response):
    with pytest.raises(WebsiteNotFoundException):
        website_store.get(
            user_id=setup['user_id'],
            website_id=setup['website_id'])


def test_it_deletes_scrapes_in_db(setup, response):
    with pytest.raises(ScrapeNotFoundException):
        scrape_store.get(
            user_id=setup['user_id'],
            website_id=setup['website_id'],
            scrape_id=setup['scrape_id'])


def test_it_deletes_screenshots_in_s3(setup, response):
    with pytest.raises(ScreenshotNotFoundException):
        screenshot_store.get(setup['scrape'])