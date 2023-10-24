from typing import List

from domain_models.domain import Website, now
from domain_models.exceptions import WebsiteNotFoundException

from ..models import WebsiteItem


class FakeWebsiteStore:

    def __init__(self):
        self.cache = {}
        
    def create(self, model: Website):
        item = WebsiteItem(
            user_id=model.user_id,
            website_id=model.website_id,
            name=model.name,
            url=model.url,
            frequency=model.frequency.value,
            version=0,
            modified_at=now())
        self.cache[(item.user_id, item.website_id)] = item

    def update(self, model: Website) -> str:
        self.create(model)

    def get(self, user_id: str, website_id: str) -> Website:
        item = self.cache.get((user_id, website_id))
        if item is None:
            raise WebsiteNotFoundException(website_id)
        return item.to_domain_model()

    def get_list(self, user_id: str) -> List[Website]:
        items = []
        for item in self.cache.values():
            if item.user_id == user_id:
                items.append(item)
                
        return [item.to_domain_model() for item in items] 

    def get_all(self) -> List[Website]:
        items = self.cache.values()
        return [item.to_domain_model() for item in items]
        
    def delete(self, user_id: str, website_id: str):
        del self.cache[(user_id, website_id)]
    