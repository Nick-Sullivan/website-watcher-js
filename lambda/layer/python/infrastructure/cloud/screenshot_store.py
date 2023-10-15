import uuid

from botocore.exceptions import ClientError
from domain_models.domain import Scrape
from domain_models.exceptions import ScreenshotNotFoundException


class S3ScreenshotStore:

    def __init__(self, s3, bucket_name):
        self.s3 = s3
        self.bucket_name = bucket_name
        
    def save(self, scrape: Scrape, screenshot: str) -> str:
        key = self._create_key(scrape)
        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=screenshot,
            ContentType='png',
        )

    def save_temporary_screenshot(self, user_id: str, screenshot: str) -> str:
        """The lifecycle of screenshots is handled by the s3 bucket"""
        key = self._create_temporary_key(user_id)

        self.s3.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=screenshot,
            ContentType='png',
        )

        return self._get(key)

    def get(self, scrape: Scrape) -> str:
        key = self._create_key(scrape)
        return self._get(key)

    def delete(self, scrape: Scrape):
        key = self._create_key(scrape)
        self.s3.delete_object(
            Bucket=self.bucket_name,
            Key=key)

    def _create_key(self, scrape: Scrape) -> str:
        return f'scrapes/user_id={scrape.user_id}'\
            + f'/website_id={scrape.website_id}'\
            + f'/{scrape.scrape_id}.png'

    def _create_temporary_key(self, user_id: str) -> str:
        file_name = f'{str(uuid.uuid4())}.png'
        return f'temp/user_id={user_id}/{file_name}'

    def _get(self, key: str) -> str:
        self._check_key_exists(key)
        return self.s3.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': key
            },
            ExpiresIn=1000)

    def _check_key_exists(self, key: str):
        try:
            self.s3.head_object(Bucket=self.bucket_name, Key=key)
        except ClientError:
            raise ScreenshotNotFoundException(key)
