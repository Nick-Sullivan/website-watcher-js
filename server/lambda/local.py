import json
import os
import sys

import boto3
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

sys.path.append('server/lambda/')
sys.path.append('server/lambda/layer/python/')

app = FastAPI(title="WebsiteWatcherJs")


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
        'requestContext': {'authorizer': {'claims': {'cognito:username': 'local'}}}
    }
    response = func(event)
    if response['statusCode'] == 200:
        return json.loads(response['body'])
    else:
        raise HTTPException(status_code=response['statusCode'], detail=json.loads(response['body']))


def load_parameters():
    load_dotenv('../../.env')

    if os.environ['IS_LOCAL'] == 'True':
        return 

    env = os.environ['ENVIRONMENT'].upper()

    prefix = f'/WebsiteWatcherJs/{env.capitalize()}'
    parameter_names = {
        f'{prefix}/ApiGateway/Url': 'API_GATEWAY_URL',
        f'{prefix}/AutomatedTester/Username': 'AUTOMATED_TESTER_USERNAME',
        f'{prefix}/AutomatedTester/Password': 'AUTOMATED_TESTER_PASSWORD',
        f'{prefix}/Cognito/ClientId': 'COGNITO_CLIENT_ID',
        f'{prefix}/Cognito/UserPool/Id': 'COGNITO_USER_POOL_ID'
    }
    ssm_client = boto3.client('ssm')
    parameters = ssm_client.get_parameters(Names=list(parameter_names), WithDecryption=True)
    for parameter in parameters['Parameters']:
        os.environ[parameter_names[parameter['Name']]] = parameter['Value']


if __name__ == "__main__":
    load_parameters()
    uvicorn.run(app, host="127.0.0.1", port=8000)
