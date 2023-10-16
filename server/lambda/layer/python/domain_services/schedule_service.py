from datetime import datetime
from math import ceil
from typing import List

from domain_models.domain import Frequency, Scrape, Website, now
from domain_models.requests import ScheduleScrapeRequest
from infrastructure import scrape_queue, scrape_store, website_store


def schedule_scrapes(request: ScheduleScrapeRequest) -> List[Website]:
    websites = website_store.get_list(request.user_id)
    websites_to_scrape = []

    print(f'websites: {websites}')
    for website in websites:
        prev_scrape = scrape_store.get_latest(website.user_id, website.website_id)
        if not (request.ignore_frequency or _is_scrape_needed(website.frequency, prev_scrape)):
            continue
        scrape_queue.create(website)
        websites_to_scrape.append(website)

    return websites_to_scrape

def _is_scrape_needed(frequency: Frequency, prev_scrape: Scrape) -> bool:
    # TODO - consider the day according to the locale
    if prev_scrape is None:
        return True
    
    time = now()
    duration = time - prev_scrape.scraped_at
    hours = duration.seconds / 60 / 60
    if frequency == Frequency.DAILY:
        return time.day != prev_scrape.scraped_at.day or hours > 24
    if frequency == Frequency.WEEKLY:
        return _week_of_month(time) != _week_of_month(prev_scrape.scraped_at) or hours > 24*7
    if frequency == Frequency.FORTNIGHTLY:
        raise NotImplementedError()
    if frequency == Frequency.MONTHLY:
        raise NotImplementedError()
    raise NotImplementedError()


def _week_of_month(dt: datetime) -> int:
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()
    return int(ceil(adjusted_dom/7.0))
