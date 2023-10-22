import os
import sys

os.environ['USE_LOCAL_INFRA'] = 'True'
sys.path.append('server/lambda/')
sys.path.append('server/lambda/layer/python/')
