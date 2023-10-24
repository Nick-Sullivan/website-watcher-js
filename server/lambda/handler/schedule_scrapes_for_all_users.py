import json

from domain_models.requests import ScheduleScrapeForAllUsersRequest
from domain_services import schedule_service


def schedule_scrapes_for_all_users(event, context=None):
    print(event)

    return _schedule_scrapes_for_all_users()


def _schedule_scrapes_for_all_users():
    
    request = ScheduleScrapeForAllUsersRequest()
    
    websites = schedule_service.schedule_scrapes_for_all_users(request)

    response = {
        'websites': [{
            'user_id': w.user_id,
            'website_id': w.website_id,
            'name': w.name,
            'url': w.url}
        for w in websites]}
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)}
