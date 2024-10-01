import ray
from ray import serve


@serve.deployment
class model_1:
    def __init__(self):
        return "hello"
    
app = model_1.bind()
