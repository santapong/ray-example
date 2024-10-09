import re
import os, sys
sys.path.append(os.path.join(os.getcwd(),'core'))

import requests
import json
import click
import logging
from logging.handlers import RotatingFileHandler

from utils import generateTemplate, HEADERS, RAY_DEPLOY_URL, Template
from utils import SessionDB

from schema.database.base import Model

from config import LOGGING_FORMAT

logging.getLogger(__name__)
logging.Formatter()


def init_deploy(session: SessionDB):
    data = generateTemplate(session=session)
    
    requests.put(url=RAY_DEPLOY_URL, headers=HEADERS, data=json.dumps(data))
    
    Template['applications'] = data
    print(json.dumps(Template, indent=4)) 
    return Template

if __name__ == '__main__':
    
    session = SessionDB()
    data = init_deploy(session=session)
    
    requests.put(url=RAY_DEPLOY_URL, headers=HEADERS, data=json.dumps(data))
    