
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class Frequency(Enum):
    HOURLY = 'HOURLY'
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    FORTNIGHTLY = 'FORTNIGHTLY'
    MONTHLY = 'MONTHLY'


@dataclass
class Website:
    user_id: str
    website_id: str
    name: str
    url: str
    frequency: Frequency


@dataclass
class Scrape:
    user_id: str
    scrape_id: str
    website_id: str
    scraped_at: datetime


def timestamp(dt: datetime):
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    
def create_unique_key() -> str:
    return str(uuid.uuid4())


def now() -> datetime:
    return datetime.now(timezone.utc)
