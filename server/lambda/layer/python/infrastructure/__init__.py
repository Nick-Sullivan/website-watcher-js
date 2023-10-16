import os

import boto3

is_local = os.environ.get('IS_LOCAL') == 'True'

if is_local:
    from .local.screenshot_store import FakeScreenshotStore
    screenshot_store = FakeScreenshotStore()

    from .local.website_store import FakeWebsiteStore
    website_store = FakeWebsiteStore()

    from .local.scrape_store import FakeScrapeStore
    scrape_store = FakeScrapeStore()

    from .local.scrape_queue import FakeScrapeQueue
    scrape_queue = FakeScrapeQueue()

    from .local.page_inspector import FakePageInspector
    page_inspector = FakePageInspector()

else:
    screenshot_bucket = os.environ.get('SCREENSHOT_BUCKET_NAME')
    if screenshot_bucket:
        from .cloud.screenshot_store import S3ScreenshotStore
        screenshot_store = S3ScreenshotStore(boto3.client('s3'), screenshot_bucket)
    else:
        screenshot_store = None
        page_inspector = None

    website_table = os.environ.get('WEBSITE_TABLE_NAME')
    if website_table:
        from .cloud.website_store import WebsiteStore
        website_store = WebsiteStore(boto3.client('dynamodb'), website_table)
    else:
        website_store = None

    scrape_table = os.environ.get('SCRAPE_TABLE_NAME')
    if scrape_table:
        from .cloud.scrape_store import ScrapeStore
        scrape_store = ScrapeStore(boto3.client('dynamodb'), scrape_table)
    else:
        scrape_store = None

    queue_url = os.environ.get('SQS_URL')
    if queue_url:
        from .cloud.scrape_queue import ScrapeQueue
        scrape_queue = ScrapeQueue(boto3.client('sqs'), queue_url)
    else:
        scrape_queue = None

    uses_playwright = os.environ.get('USES_PLAYWRIGHT') == 'True'
    if uses_playwright:
        from .cloud.page_inspector import PageInspector
        page_inspector = PageInspector()
    else:
        page_inspector = None
    