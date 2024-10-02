import ray
from ray import serve

@serve.deployment
class model_6:
    def __init__(self) -> None:
        import emoji
        return { "msg" : emoji.__version__ }
    
Deploy = model_6