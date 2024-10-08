import os, sys
sys.path.append(os.path.join(os.getcwd(),'core'))

import requests
import json
import click
import logging
from logging.handlers import RotatingFileHandler

from utils import generateTemplate, HEADERS, RAY_DEPLOY_URL
from utils import SessionDB

from schema.database.base import Model

from config import LOGGING_FORMAT

logging.getLogger(__name__)
logging.Formatter()

session = SessionDB()


def init_deploy(session: SessionDB):
    data = generateTemplate(session=session)
    json_data = json.dumps(data, indent=4)
    
    requests.put(url=RAY_DEPLOY_URL, headers=HEADERS, data=json.dumps(data))
    
    print(json_data) 

if __name__ == '__main__':
    init_deploy(session=session)
    