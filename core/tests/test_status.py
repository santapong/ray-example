import ray
from ray import serve

from pprint import pprint

status = serve.status()

model = 'model_1'

# pprint(f'This is status {status}')

# Check Status
pprint(f'This is application {model} {status.applications[model].status}')

pprint(f'This is Deployment {model} {status.applications[model].deployments[model].status}')
