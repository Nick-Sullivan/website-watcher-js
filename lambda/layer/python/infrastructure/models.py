from dataclasses import asdict, dataclass, fields
from datetime import datetime, timezone

from boto3.dynamodb.types import TypeDeserializer, TypeSerializer
from dateutil import parser
from domain_models.domain import Frequency, Scrape, Website, now, timestamp


@dataclass
class DatabaseItem:
    version: int
    modified_at: datetime

    def serialise(self) -> str:
        serialiser = TypeSerializer()
        item_dict = asdict(self)
        for field in fields(self):
            if field.type == datetime:
                item_dict[field.name] = timestamp(item_dict[field.name])
        return serialiser.serialize(item_dict)['M']

    @classmethod
    def deserialise(cls, serialised: str):
        deserialiser = TypeDeserializer()
        item_dict = deserialiser.deserialize({'M': serialised})
        for field in fields(cls):
            if field.type == datetime:
                item_dict[field.name] = parser.parse(item_dict[field.name]).replace(tzinfo=timezone.utc)

        return cls(**item_dict)


@dataclass
class WebsiteItem(DatabaseItem):
    user_id: str
    website_id: str
    name: str
    url: str
    frequency: str

    def to_domain_model(self) -> Website:
        return Website(
            user_id=self.user_id,
            website_id=self.website_id,
            name=self.name,
            url=self.url,
            frequency=Frequency(self.frequency))


@dataclass
class ScrapeItem(DatabaseItem):
    partition_key: str
    scrape_id: str
    scraped_at: datetime

    def to_domain_model(self) -> Scrape:
        user_id, website_id = self.from_partition_key(self.partition_key)
        return Scrape(
            user_id=user_id,
            scrape_id=self.scrape_id,
            website_id=website_id,
            scraped_at=self.scraped_at)

    @classmethod
    def from_domain_model(cls, model: Scrape):
        partition_key = cls.to_partition_key(model.user_id, model.website_id)
        return ScrapeItem(
            partition_key=partition_key,
            scrape_id=model.scrape_id,
            scraped_at=model.scraped_at,
            version=0,
            modified_at=now())

    @staticmethod
    def to_partition_key(user_id: str, website_id: str) -> str:
        return user_id + '#' + website_id
    
    @staticmethod
    def from_partition_key(partition_key: str) -> (str,str):
        split = partition_key.split('#')
        user_id = split[0]
        website_id = split[1]
        return user_id, website_id
