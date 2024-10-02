import ray
from ray import serve

import s3fs

@serve.deployment(ray_actor_options={ 
        "runtime_env": {"pip":[
            "numpy==1.26.4"
        ]}
    })
class model_5:
    def __init__(self):
        return "Hello"
    

# NOTE:
# IF in .zip file have 1.Python code, 2.Model, 3.Requirement

# Composite Model