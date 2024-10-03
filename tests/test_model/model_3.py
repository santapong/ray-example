import ray
from ray import serve


@serve.deployment
class model_3:
    def __init__(self):
        return "hello"
    
Deploy = model_3