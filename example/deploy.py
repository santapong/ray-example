import s3fs
import importlib.util

import ray
from ray import serve
from ray.runtime_env import RuntimeEnv

from dotenv import load_dotenv


load_dotenv()


def deploy(name: str):
    """Read Python module from S3 and import it dynamically."""
    # Use s3fs to read the file directly from S3
    route_prefix = f'/{name}'
    s3_path = f's3://santapong/test/{name}.py'
    
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(s3_path, 'r') as f:
        file_content = f.read()

    # Save the file content to a temporary file
    local_file_path = f'/tmp/{name}.py'
    with open(local_file_path, 'w') as local_file:
        local_file.write(file_content)

    # Import the module dynamically using importlib
    spec = importlib.util.spec_from_file_location(name, local_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    imported_module = module
    
    # Step 2: Access the 'app' variable from the imported module
    deploy = imported_module.Deploy

    runtime_env = RuntimeEnv(pip=['emoji==2.13.2'])

    app = deploy.options(name=name,ray_actor_options={"num_cpus": 1.0,"runtime_env":runtime_env}).bind()
    # Step 3: Use the 'app' with Ray Serve
    serve.run(app, route_prefix=route_prefix, name=name)
    
    return {"msg":f"deploy {name} sucessfully"}

if __name__ == '__main__':
    deploy('model_6')