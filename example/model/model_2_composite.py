import ray
from ray import serve
from ray.runtime_env import RuntimeEnv
from ray.serve.handle import DeploymentHandle
from dotenv import load_dotenv

load_dotenv()

import ray
from ray import serve
from ray.serve.handle import DeploymentHandle, DeploymentResponse

@serve.deployment
class Downstream:
    def say_hi(self, message: str):
        self._message = message
        return f"Hello {message}!"
        
        
@serve.deployment
class Downstream_2:
    def say_hey(self, message: str):
        return f"Hello {message}"

@serve.deployment
class Ingress:
    def __init__(self, handle: DeploymentHandle):
        self._downstream_handle = handle

    async def __call__(self, name: str) -> str:
        response = self._handle.say_hi.remote(name)
        return await response
    
Deploy = {'main':[Ingress],
          "sub":[Downstream, Downstream_2]}

# sub_application = [sub_Deploy.bind() for sub_Deploy in Deploy.get('sub')]

# main_application = Ingress.bind(sub_application)


# print(main_application)

# serve.run(main_application, route_prefix='/main', name='main')

# print("Deploy successful")