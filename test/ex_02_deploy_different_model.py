import ray
from ray import serve

import time

from pprint import pprint

@serve.deployment
class model_1:
    def __init__(self):
        print("Hello")
        
    def predict(self):
        print("predicted")
        

@serve.deployment
class model_2:
    def __init__(self):
        print("Hello")
        
    def predict(self):
        print("predicted")

# Prepare for deploy        
model_1_app = model_1.bind()
model_2_app = model_2.bind()

serve.run(model_1_app, route_prefix='/model_1', name='model_1')

print('sleep for 5 second')
time.sleep(5)

serve.run(model_2_app, route_prefix='/mode_2', name='model_2')

pprint(serve.status())