import ray
from ray import serve
from ray.serve.handle import DeploymentHandle

import s3fs

import ray
from ray import serve
from ray.serve.handle import DeploymentHandle, DeploymentResponse

@serve.deployment
class Downstream:
    def say_hi(self, message: str):
        return f"Hello {message}!"
        self._message = message

@serve.deployment
class Ingress:
    def __init__(self, handle: DeploymentHandle):
        self._downstream_handle = handle

    async def __call__(self, name: str) -> str:
        response = self._handle.say_hi.remote(name)
        return await response

Deploys = [Downstream, Ingress]

app = Ingress.bind(Downstream.bind())
handle: DeploymentHandle = serve.run(app)
response = handle.remote("world")
assert response.result() == "Hello world!"