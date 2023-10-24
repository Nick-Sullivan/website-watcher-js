from typing import List

from boto3.dynamodb.types import TypeSerializer
from domain_models.domain import Website, now
from domain_models.exceptions import WebsiteNotFoundException

from ..models import WebsiteItem


class WebsiteStore:

    def __init__(self, client, table_name):
        self.client = client
        self.table_name = table_name
        self.serialiser = TypeSerializer()

    def create(self, model: Website):
        assert isinstance(model, Website)
        item = WebsiteItem(
            user_id=model.user_id,
            website_id=model.website_id,
            name=model.name,
            url=model.url,
            frequency=model.frequency.value,
            version=0,
            modified_at=now())

        self.client.put_item(
            TableName=self.table_name,
            Item=item.serialise(),
            ConditionExpression='attribute_not_exists(website_id)')

    def update(self, model: Website):
        item = WebsiteItem(
            user_id=model.user_id,
            website_id=model.website_id,
            name=model.name,
            url=model.url,
            frequency=model.frequency.value,
            version=0,
            modified_at=now())

        self.client.put_item(
            TableName=self.table_name,
            Item=item.serialise(),
            ConditionExpression='attribute_exists(website_id)')

    def get(self, user_id: str, website_id: str) -> Website:
        response = self.client.get_item(
            TableName=self.table_name,
            Key={
                'user_id': {'S': str(user_id)},
                'website_id': {'S': str(website_id)}})
        if 'Item' not in response:
            raise WebsiteNotFoundException(website_id)
        item = WebsiteItem.deserialise(response['Item'])
        return item.to_domain_model()

    def get_list(self, user_id: str) -> List[Website]:
        response = self.client.query(
            TableName=self.table_name,
            KeyConditionExpression='user_id = :user_id',
            ExpressionAttributeValues={':user_id': {'S': str(user_id)}}
        )
        items = [WebsiteItem.deserialise(item) for item in response['Items']]
        items.sort(key=lambda x: x.name)
        return [item.to_domain_model() for item in items]

    def get_all(self) -> List[Website]:
        response = self.client.scan(
            TableName=self.table_name,
        )
        items = [WebsiteItem.deserialise(item) for item in response['Items']]
        items.sort(key=lambda x: x.name)
        return [item.to_domain_model() for item in items]

    def delete(self, user_id: str, website_id: str):
        key = {
            'user_id': user_id,
            'website_id': website_id}

        serialised = self.serialiser.serialize(key)['M']

        self.client.delete_item(
            TableName=self.table_name,
            Key=serialised)
