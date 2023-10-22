import os
import sys

import boto3
from dotenv import load_dotenv

os.environ['USE_LOCAL_INFRA'] = 'False'

sys.path.append('server/lambda/')
sys.path.append('server/lambda/layer/python/')

# If this is CICD, the environment to test is passed by environment variables.
# If this is local, the environment to test is in the root .env
is_cicd = os.environ.get('IS_CICD', 'False').lower() == 'true'
if not is_cicd:
    load_dotenv('.env')

env = os.environ['ENVIRONMENT']

prefix = f'/WebsiteWatcherJs/{env.capitalize()}'
parameter_names = {
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
parameters = ssm_client.get_parameters(Names=list(parameter_names), WithDecryption=True)
for parameter in parameters['Parameters']:
    os.environ[parameter_names[parameter['Name']]] = parameter['Value']
