import uuid

from domain_models.domain import Scrape
from domain_models.exceptions import ScreenshotNotFoundException


class FakeScreenshotStore:

    def __init__(self):
        self.cache = {}
        self.temp_cache = {}
    
    def save(self, scrape: Scrape, screenshot: str) -> str:
        self.cache[(scrape.user_id, scrape.scrape_id)] = screenshot

    def save_temporary_screenshot(self, user_id: str, screenshot: str) -> str:
        if user_id not in self.temp_cache:
            self.temp_cache[user_id] = {}

        key = str(uuid.uuid4())

        self.temp_cache[user_id][key] = screenshot

        return key

    def get(self, scrape: Scrape) -> str:
        item = self.cache.get((scrape.user_id, scrape.scrape_id))
        if item is None:
            raise ScreenshotNotFoundException(f'{(scrape.user_id, scrape.scrape_id)}')
        return item

    def get_temporary_screenshot(self, user_id: str, key: str) -> str:
        return self.temp_cache[user_id][key]
    
    def delete(self, scrape: Scrape):
        del self.cache[(scrape.user_id, scrape.scrape_id)]
        