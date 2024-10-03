import ray
from ray import serve


@serve.deployment
class model_4:
    def __init__(self):
        return "hello"
    
Deploy = model_4