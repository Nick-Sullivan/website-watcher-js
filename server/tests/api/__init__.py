import os
import sys

import boto3
from dotenv import load_dotenv

sys.path.append('server/lambda/')
sys.path.append('server/lambda/layer/python/')

# If this is CICD, the environment to test is passed by environment variables.
# If this is local, the environment to test is in the root .env
is_cicd = os.environ.get('IS_CICD', False)
if not is_cicd:
    load_dotenv('.env')

env = os.environ['ENVIRONMENT']

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
