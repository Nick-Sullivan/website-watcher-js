from typing import List

from domain_models.domain import Website, create_unique_key
from domain_models.requests import (
    CreateWebsiteRequest,
    DeleteWebsiteRequest,
    GetWebsiteRequest,
    GetWebsitesRequest,
    UpdateWebsiteRequest,
)
from infrastructure import scrape_store, screenshot_store, website_store


def create_website(request: CreateWebsiteRequest) -> str:
    website = Website(
        user_id=request.user_id,
        website_id=create_unique_key(),
        name=request.name,
        url=request.url,
        frequency=request.frequency)
    website_store.create(website)
    return website.website_id


def update_website(request: UpdateWebsiteRequest) -> Website:
    website = website_store.get(request.user_id, request.website_id)
    new_website = Website(
        user_id=website.user_id,
        website_id=website.website_id,
        name=request.name,
        url=request.url,
        frequency=request.frequency)
    website_store.update(new_website)
    return website.website_id


def get_website(request: GetWebsiteRequest) -> Website:
    return website_store.get(request.user_id, request.website_id)


def get_websites(request: GetWebsitesRequest) -> List[Website]:
    return website_store.get_list(request.user_id)
    

def delete_website(request: DeleteWebsiteRequest):
    website_store.get(request.user_id, request.website_id)  # raise exception if not exists
    scrapes = scrape_store.get_list(request.user_id, request.website_id)
    for scrape in scrapes:
        screenshot_store.delete(scrape)
        scrape_store.delete(scrape.user_id, scrape.website_id, scrape.scrape_id)
    website_store.delete(request.user_id, request.website_id)
    