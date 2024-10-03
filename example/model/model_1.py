import starlette.requests
import requests
from ray import serve



@serve.deployment
class Counter:
    def __init__(self):
        pass
    
    def __call__(self, request: starlette.requests.Request):
        from reletional_file import hello
        
        return {"msg":f"{hello()}",
                "version":"Test"}

Deploy = Counter