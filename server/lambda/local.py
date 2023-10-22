"""Hosts API endpoints locally"""

import json
import os
import sys
from typing import Annotated, Dict

import boto3
import jwt
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

sys.path.append('lambda/')
sys.path.append('lambda/layer/python/')


app = FastAPI(title="WebsiteWatcherJs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def parse_user(req: Request) -> str:
    token = req.headers['authentication'].split(' ')[-1]
    token_header = jwt.get_unverified_header(token)
    decoded = jwt.decode(jwt=token, algorithms=[token_header['alg']], options={"verify_signature": False})
    user = decoded['cognito:username']
    return user


@app.post("/websites")
def create_websites(body: Dict):
    import handler.create_website
    return invoke(handler.create_website.create_website, body)


@app.get("/websites")
def get_websites(user: Annotated[str, Depends(parse_user)]):
    import handler.get_websites
    return invoke(handler.get_websites.get_websites, body={}, user=user)


@app.get("/websites/{website_id}")
def get_website(website_id, user: Annotated[str, Depends(parse_user)]):
    import handler.get_website
    pathParams = {'website_id': website_id}
    return invoke(handler.get_website.get_website, body={}, user=user, pathParams=pathParams)


@app.delete("/websites/{website_id}")
def delete_websites(website_id, user: Annotated[str, Depends(parse_user)]):
    import handler.delete_website
    pathParams = {'website_id': website_id}
    return invoke(handler.delete_website.delete_website, body={}, user=user, pathParams=pathParams)


def invoke(func, body: Dict, user: str, pathParams=None):
    
    event = {
        'body': json.dumps(body),
        'requestContext': {'authorizer': {'claims': {'cognito:username': user}}},
        'pathParameters': pathParams,
    }
    response = func(event)
    if response['statusCode'] == 200:
        if 'body' in response:
            return json.loads(response['body'])
    else:
        raise HTTPException(status_code=response['statusCode'], detail=json.loads(response['body']))


def load_parameters():
    load_dotenv('../.env')

    if os.environ.get('USE_LOCAL_INFRA', 'false').lower() == 'true':
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
