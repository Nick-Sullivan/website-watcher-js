
import pytest
from domain_models.domain import create_unique_key

from .endpoints import preview_website


@pytest.fixture(scope='module')
def response():
    user_id = create_unique_key()
    preview_req = {'user_id': user_id, 'url': 'https://google.com'}
    preview_res = preview_website(preview_req)
    yield preview_res


@pytest.fixture
def response_body(response):
    yield response.json()


def test_it_returns_status_200(response):
    assert response.status_code == 200


def test_it_returns_user_id(response_body):
    assert 'user_id' in response_body


def test_it_returns_a_url(response_body):
    assert 'screenshot_url' in response_body

