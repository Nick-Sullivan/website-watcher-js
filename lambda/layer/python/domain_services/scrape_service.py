from typing import List

from domain_models.domain import Scrape, now, timestamp
from domain_models.requests import (
    GetScrapesRequest,
    GetScreenshotRequest,
    PreviewWebsiteRequest,
    ScrapeWebsiteRequest,
)
from infrastructure import (
    page_inspector,
    scrape_store,
    screenshot_store,
    website_store,
)


def preview(request: PreviewWebsiteRequest) -> str:
    with page_inspector.load_page(request.url) as page:
        screenshot = page.screenshot(full_page=True)

    screenshot_url = screenshot_store.save_temporary_screenshot(
        user_id=request.user_id,
        screenshot=screenshot)

    return screenshot_url


def scrape_website(request: ScrapeWebsiteRequest) -> Scrape:
    website = website_store.get(request.user_id, request.website_id)

    with page_inspector.load_page(website.url) as page:
        screenshot = page.screenshot(full_page=True)

    scraped_at = now()
    scrape_id = timestamp(scraped_at)
    scrape = Scrape(
        user_id=request.user_id,
        scrape_id=scrape_id,
        website_id=website.website_id,
        scraped_at=scraped_at)

    scrape_store.create(scrape)

    screenshot_store.save(scrape=scrape, screenshot=screenshot)
    
    return scrape


def get_scrape(request: GetScrapesRequest) -> Scrape:
    return scrape_store.get(request.user_id, request.website_id, request.scrape_id)


def get_scrapes(request: GetScrapesRequest) -> List[Scrape]:
    return scrape_store.get_list(request.user_id, request.website_id)
    

def get_screenshot(request: GetScreenshotRequest) -> str:
    scrape = scrape_store.get(
        user_id=request.user_id,
        website_id=request.website_id,
        scrape_id=request.scrape_id)
    return screenshot_store.get(scrape)
