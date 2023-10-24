

import json
import os
from datetime import datetime, timezone

import boto3

eventbridge = boto3.client('events')
environment = os.environ['ENVIRONMENT'].title()

def publish_scrape_schedule_event():
    response = eventbridge.put_events(
        Entries=[{
            'Time': datetime.now(timezone.utc),
            'Source': 'ApiTests',
            'DetailType': f'{environment}-ScrapesForAllUsersRequested',
            'Detail': json.dumps({}),
        }]
    )
    return response
