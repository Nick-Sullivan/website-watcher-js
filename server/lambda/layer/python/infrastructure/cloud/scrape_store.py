from typing import List

from boto3.dynamodb.types import TypeSerializer
from domain_models.domain import Scrape
from domain_models.exceptions import ScrapeNotFoundException

from ..models import ScrapeItem


class ScrapeStore:

    def __init__(self, client, table_name):
        self.client = client
        self.table_name = table_name
        self.serialiser = TypeSerializer()

    def create(self, model: Scrape):
        assert isinstance(model, Scrape)
        item = ScrapeItem.from_domain_model(model)

        self.client.put_item(
            TableName=self.table_name,
            Item=item.serialise(),
            ConditionExpression='attribute_not_exists(partition_key)')

    def get(self, user_id: str, website_id: str, scrape_id: str) -> Scrape:
        partition_key = ScrapeItem.to_partition_key(user_id, website_id)
        response = self.client.get_item(
            TableName=self.table_name,
            Key={
                'partition_key': {'S': str(partition_key)},
                'scrape_id': {'S': str(scrape_id)}})
        if 'Item' not in response:
            raise ScrapeNotFoundException(scrape_id)
        item = ScrapeItem.deserialise(response['Item'])
        return item.to_domain_model()

    def get_latest(self, user_id: str, website_id: str) -> Scrape:
        """Assumes the sort_key is stored alphabetically"""
        partition_key = ScrapeItem.to_partition_key(user_id, website_id)
        response = self.client.query(
            TableName=self.table_name,
            KeyConditionExpression='partition_key = :partition_key',
            ExpressionAttributeValues={':partition_key': {'S': str(partition_key)}},
            ScanIndexForward=False,
            Limit=1,
        )
        if not response['Items']:
            return None
        item = ScrapeItem.deserialise(response['Items'][0])
        return item.to_domain_model()

    def get_list(self, user_id: str, website_id: str) -> List[Scrape]:
        partition_key = ScrapeItem.to_partition_key(user_id, website_id)
        response = self.client.query(
            TableName=self.table_name,
            KeyConditionExpression='partition_key = :partition_key',
            ExpressionAttributeValues={':partition_key': {'S': partition_key}})
        items = [ScrapeItem.deserialise(item) for item in response['Items']]
        items.sort(key=lambda x: x.scraped_at)
        return [item.to_domain_model() for item in items]

    def delete(self, user_id: str, website_id: str, scrape_id: str):
        partition_key = ScrapeItem.to_partition_key(user_id, website_id)
        key = {
            'partition_key': partition_key,
            'scrape_id': scrape_id}

        serialised = self.serialiser.serialize(key)['M']

        self.client.delete_item(
            TableName=self.table_name,
            Key=serialised)
    