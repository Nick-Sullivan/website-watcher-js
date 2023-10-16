import os
import sys

os.environ['IS_LOCAL'] = 'True'
# os.environ['SCREENSHOT_BUCKET_NAME'] = 'website-watcher2-stage'
# os.environ['WEBSITE_TABLE_NAME'] = 'WebsiteWatcher2StageWebsites'
# os.environ['SCRAPE_TABLE_NAME'] = 'WebsiteWatcher2StageScrapes'
# os.environ['SQS_URL'] = 'https://sqs.ap-southeast-2.amazonaws.com/314077822992/WebsiteWatcher2Stage-ScrapeQueue'
# os.environ['USES_PLAYWRIGHT'] = 'True'
sys.path.append('server/lambda/')
sys.path.append('server/lambda/layer/python/')
