import os
import sys

import boto3

sys.path.append('server/lambda/')
sys.path.append('server/lambda/layer/python/')

ssm_client = boto3.client('ssm')

prefix = 'WEBSITE_WATCHER_JS_'
parameter_names = [
    f'{prefix}API_GATEWAY_URL',
    f'{prefix}AUTOMATED_TESTER_USERNAME',
    f'{prefix}AUTOMATED_TESTER_PASSWORD',
    f'{prefix}COGNITO_CLIENT_ID',
    f'{prefix}COGNITO_USER_POOL_ID'
]
parameters = ssm_client.get_parameters(Names=parameter_names, WithDecryption=True)
for parameter in parameters['Parameters']:
    os.environ[parameter['Name'].removeprefix(prefix)] = parameter['Value']

# from dotenv import load_dotenv
# load_dotenv('terraform/environments/stage/infrastructure/output.env')