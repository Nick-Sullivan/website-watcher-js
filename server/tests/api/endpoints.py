
import json
import os
from functools import lru_cache

import boto3
import requests

base_url = os.environ['API_GATEWAY_URL']
client_id = os.environ['COGNITO_CLIENT_ID']
username = os.environ['AUTOMATED_TESTER_USERNAME']
password = os.environ['AUTOMATED_TESTER_PASSWORD']
cognito = boto3.client('cognito-idp')


@lru_cache
def authenticate():
    response = cognito.initiate_auth(
        ClientId=client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
        }
    )
    id_token = response['AuthenticationResult']['IdToken']
    return id_token


def _post(endpoint, data):
    headers = {'Authorization': f'Bearer {authenticate()}'}
    return requests.request(
        'POST',
        f'{base_url}/{endpoint}',
        data=json.dumps(data),
        headers=headers)


def _delete(endpoint):
    headers = {'Authorization': f'Bearer {authenticate()}'}
    return requests.request('DELETE', f'{base_url}/{endpoint}', headers=headers)


def _get(endpoint):
    headers = {'Authorization': f'Bearer {authenticate()}'}
    return requests.request('GET', f'{base_url}/{endpoint}', headers=headers)


def _options(endpoint, origin):
    headers = {'origin': origin}
    return requests.request('OPTIONS', f'{base_url}/{endpoint}', headers=headers)


def _put(endpoint, data):
    headers = {'Authorization': f'Bearer {authenticate()}'}
    return requests.request(
        'PUT',
        f'{base_url}/{endpoint}',
        data=json.dumps(data),
        headers=headers)


def options_website(origin):
    return _options('websites', origin)


def create_website(request):
    return _post('websites', request)


def update_website(request):
    website_id = request['website_id']
    return _put(f'websites/{website_id}', request)


def delete_website(request):
    website_id = request['website_id']
    return _delete(f'websites/{website_id}')


def scrape_website(request):
    website_id = request['website_id']
    return _post(f'websites/{website_id}/scrape', request)


def get_screenshot(request):
    website_id = request['website_id']
    scrape_id = request['scrape_id']
    return _get(f'websites/{website_id}/scrapes/{scrape_id}/screenshot')


def get_scrape(request):
    website_id = request['website_id']
    scrape_id = request['scrape_id']
    return _get(f'websites/{website_id}/scrapes/{scrape_id}')


def get_scrapes(request):
    website_id = request['website_id']
    return _get(f'websites/{website_id}/scrapes')


def get_website(request):
    website_id = request['website_id']
    return _get(f'websites/{website_id}')


def get_websites():
    return _get('websites')


def preview_website(request):
    return _post('websites/preview', request)


def schedule_scrapes(request):
    return _post('websites/scrape', request)
    