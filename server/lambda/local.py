"""Hosts API endpoints locally"""

import json
import os
import sys

import boto3
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

sys.path.append('server/lambda/')
sys.path.append('server/lambda/layer/python/')

app = FastAPI(title="WebsiteWatcherJs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/websites")
def create_websites():
    import handler.create_website
    return invoke(handler.create_website.create_website, {})


@app.get("/websites")
def get_websites():
    import handler.get_websites
    return invoke(handler.get_websites.get_websites, {})


def invoke(func, body):
    event = {
        'body': json.dumps(body),
        'requestContext': {'authorizer': {'claims': {'cognito:username': os.environ['COGNITO_USER_ID']}}}
    }
    response = func(event)
    if response['statusCode'] == 200:
        return json.loads(response['body'])
    else:
        raise HTTPException(status_code=response['statusCode'], detail=json.loads(response['body']))


def load_parameters():
    load_dotenv('../../.env')

    if os.environ['USE_LOCAL_INFRA'].lower() == 'true':
        return 

    env = os.environ['ENVIRONMENT'].upper()

    prefix = f'/WebsiteWatcherJs/{env.capitalize()}'
    names = {
        f'{prefix}/ApiGateway/Url': 'API_GATEWAY_URL',
        f'{prefix}/AutomatedTester/Username': 'AUTOMATED_TESTER_USERNAME',
        f'{prefix}/AutomatedTester/Password': 'AUTOMATED_TESTER_PASSWORD',
        f'{prefix}/Cognito/ClientId': 'COGNITO_CLIENT_ID',
        f'{prefix}/Cognito/UserPool/Id': 'COGNITO_USER_POOL_ID',
        f'{prefix}/S3/Snapshot/Name': 'SCREENSHOT_BUCKET_NAME',
        f'{prefix}/Db/Website/Name': 'WEBSITE_TABLE_NAME',
        f'{prefix}/Db/Scrape/Name': 'SCRAPE_TABLE_NAME',
        f'{prefix}/Sqs/Url': 'SQS_URL',
    }
    ssm_client = boto3.client('ssm')
    parameters = ssm_client.get_parameters(Names=list(names), WithDecryption=True)
    for parameter in parameters['Parameters']:
        os.environ[names[parameter['Name']]] = parameter['Value']


if __name__ == "__main__":
    load_parameters()
    uvicorn.run(app, host="127.0.0.1", port=8000)
