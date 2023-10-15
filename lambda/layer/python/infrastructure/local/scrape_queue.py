
from domain_models.domain import Website


class FakeScrapeQueue:

    def __init__(self):
        self.cache = {}

    def create(self, website: Website):
        self.cache[(website.user_id, website.website_id)] = website

    def get_record(self, user_id: str, website_id: str) -> Website:
        return self.cache[(user_id, website_id)]