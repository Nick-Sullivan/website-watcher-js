from typing import List

from domain_models.domain import Scrape
from domain_models.exceptions import ScrapeNotFoundException

from ..models import ScrapeItem


class FakeScrapeStore:

    def __init__(self):
        self.cache = {}
        
    def create(self, model: Scrape) -> str:
        item = ScrapeItem.from_domain_model(model)
        self.cache[(item.partition_key, item.scrape_id)] = item

    def get(self, user_id: str, website_id: str, scrape_id: str) -> Scrape:
        partition_key = ScrapeItem.to_partition_key(user_id, website_id)
        item = self.cache.get((partition_key, scrape_id))
        if item is None:
            raise ScrapeNotFoundException(scrape_id)
        return item.to_domain_model()

    def get_latest(self, user_id: str, website_id: str) -> Scrape:
        scrapes = self.get_list(user_id, website_id)
        if not scrapes:
            return None
        scrapes.sort(key=lambda x: x.scraped_at, reverse=True)
        return scrapes[0]

    def get_list(self, user_id: str, website_id: str) -> List[Scrape]:
        partition_key = ScrapeItem.to_partition_key(user_id, website_id)
        items = []
        for item in self.cache.values():
            if item.partition_key == partition_key:
                items.append(item)
                
        return [item.to_domain_model() for item in items]

    def delete(self, user_id: str, website_id: str, scrape_id: str):
        partition_key = ScrapeItem.to_partition_key(user_id, website_id)
        del self.cache[(partition_key, scrape_id)]
    