from typing import Any
import ray
from ray import serve



@serve.deployment
class model_7:
    def __init__(self) -> None:
        from reletional_file import hello
        
        print("hello")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return hello()
    
Deploy = model_7