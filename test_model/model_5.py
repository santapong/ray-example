import ray
from ray import serve


@serve.deployment
class model_5:
    def __init__(self):
        return "hello"
    
Deploy = model_5