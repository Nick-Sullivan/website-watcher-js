import json

from domain_models.domain import Website


class ScrapeQueue:

    def __init__(self, sqs, url):
        self.sqs = sqs
        self.url = url
        self.records = {}

    def create(self, website: Website):
        message = {
            'user_id': website.user_id,
            'website_id': website.website_id}

        self.sqs.send_message(
            QueueUrl=self.url,
            MessageBody=json.dumps(message))
        
        self.records[(website.user_id, website.website_id)] = website

    def get_record(self, user_id: str, website_id: str) -> Website:
        return self.records[(user_id, website_id)]
    