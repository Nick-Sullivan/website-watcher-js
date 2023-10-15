from dataclasses import dataclass

from .domain import Frequency


@dataclass
class PreviewWebsiteRequest:
    user_id: str
    url: str


@dataclass
class CreateWebsiteRequest:
    user_id: str
    name: str
    url: str
    frequency: Frequency


@dataclass
class UpdateWebsiteRequest:
    user_id: str
    website_id: str
    name: str
    url: str
    frequency: Frequency


@dataclass
class GetWebsiteRequest:
    user_id: str
    website_id: str

@dataclass
class GetWebsitesRequest:
    user_id: str


@dataclass
class ScrapeWebsiteRequest:
    user_id: str
    website_id: str


@dataclass
class ScheduleScrapeRequest:
    user_id: str
    ignore_frequency: bool
    

@dataclass
class GetScrapeRequest:
    user_id: str
    website_id: str
    scrape_id: str


@dataclass
class GetScrapesRequest:
    user_id: str
    website_id: str
    
    
@dataclass
class DeleteWebsiteRequest:
    user_id: str
    website_id: str


@dataclass
class GetScreenshotRequest:
    user_id: str
    website_id: str
    scrape_id: str
    