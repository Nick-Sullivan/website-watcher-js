import sys

from dotenv import load_dotenv

sys.path.append('server/lambda/')
sys.path.append('server/lambda/layer/python/')

load_dotenv('terraform/environments/stage/infrastructure/output.env')