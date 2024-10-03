import ray
from ray import serve


@serve.deployment
class model_2:
    def __init__(self):
        return "hello"
    
app = model_2.bind()