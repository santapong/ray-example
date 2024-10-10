import ray
from ray import serve


@serve.deployment
class model_3:
    def __init__(self):
        pass  # Initialize your model or resources here
    
    def __call__(self):
        return "hello"

# Bind the deployment


Deploy = model_3

