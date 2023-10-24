
import pytest

from .endpoints import delete_website, get_websites


@pytest.fixture(scope='module')
def setup():
    response = get_websites()
    response_body = response.json()
    website_ids = [w['website_id'] for w in response_body['websites']]
    try:
        yield {'website_ids': website_ids}
    finally:
        for website_id in website_ids:
            delete_req = {'website_id': website_id}
            delete_website(delete_req)


def test_there_are_no_websites_from_previous_test_runs(setup):
    assert len(setup['website_ids']) == 0
