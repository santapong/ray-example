import os, sys

sys.path.append(os.path.join(os.getcwd(),'core'))

from utils.session import SessionDB
import json
import logging
from logging.handlers import RotatingFileHandler

from typing import Dict
from config import RAY_DASHBOARD_URL

from schema.database.base import Model

RAY_API_PATH = 'api/serve/applications/'
RAY_DEPLOY_URL = "/".join([RAY_DASHBOARD_URL, RAY_API_PATH])

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

Template = {
    'applications':[]
}


def generateTemplate(session: SessionDB) -> Dict:
    """
    Args:
        name (str): _description_
        route_prefix (str): _description_
        runtime_env (str): _description_
        session (SessionDB): _description_

    Returns:
        Dict: _description_
    """
    # Output all Application
    applications = []
    
    # Query data from database
    models = session.getdata(Model)
    
    for model in models:
        # Create a dictionary for runtime_env instead of a set
        application = {  # Changed from "application" to "applications" to match your original structure
                "name": model.model_name,
                "route_prefix": model.route_prefix,
                "import_path": f"{model.model_name}:app",
                "runtime_env": {
                    "working_dir": model.working_dir  # Create a proper dictionary here
                },
                "deployments": [
                    {'name': 'main', 'user_config': {'app': f'{model.model_name}'}},
                    {'name': 'sub', 'user_config': {'app': f'{model.model_name}'}}
                ]
            }
        applications.append(application)
    
    return applications

if __name__ == '__main__':
    data = generateTemplate()
    json_data = json.dumps(data, indent=4)
    print(json_data)  # Print json_data to see the JSON representation
