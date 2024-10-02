from typing import Any
import ray
from ray import serve

from reletional_file import hello

@serve.deployment
class model_7:
    def __init__(self) -> None:
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return hello()
    
Deploy = model_7