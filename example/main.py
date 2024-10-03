import uvicorn
import s3fs
import importlib.util
import os
import zipfile
import types
import io

from dotenv import load_dotenv

from pydantic import BaseModel

import ray
from ray import serve
from ray.runtime_env import RuntimeEnv
load_dotenv()

from fastapi import FastAPI

class DeployInput(BaseModel):
    name: str
    s3_path: str
    route_prefix: str

app = FastAPI()


@app.post('/test')
async def deploy():
    return {"Hello":"world"}

@app.post('/register')
async def register(name: str, s3_path: str=None):
    """Read Python module from S3 and import it dynamically."""
    # Use s3fs to read the file directly from S3
    route_prefix = f'/{name}'
    s3_path = f's3://santapong/test/{name}.py'
    
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(s3_path, 'r') as f:
        file_content = f.read()

    # Save the file content to a temporary file
    local_file_path = f'./tmp/{name}.py'
    with open(local_file_path, 'w') as local_file:
        local_file.write(file_content)

    # Import the module dynamically using importlib
    spec = importlib.util.spec_from_file_location(name, local_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    imported_module = module
    
    
    # Step 2: Access the 'app' variable from the imported module
    deploy = imported_module.Deploy

    runtime_env = RuntimeEnv()

    app = deploy.options(name=name,ray_actor_options={}).bind()
    # Step 3: Use the 'app' with Ray Serve
    serve.run(app, route_prefix=route_prefix, name=name)
    
    return {"msg":f"deploy {name} sucessfully"}

@app.post('/deploy/runtime_env')
async def deploy(name: str, s3_path: str=None, runtime_env: str=None, working_dir: str=None):
    """Read Python module from S3 and import it dynamically."""
    # Use s3fs to read the file directly from S3
     # Initialize S3 filesystem
    s3 = s3fs.S3FileSystem(anon=False)
    s3_path = f's3://santapong/test_zip/{name}.zip'
    route_prefix = f'/{name}'
    # Read the .zip file content from S3
    with s3.open(s3_path, 'rb') as s3_file:
        zip_data = s3_file.read()

    # Open the zip file in memory
    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
        # List all files in the zip
        if f'{name}.py' in z.namelist():
            # Read the content of the desired Python file
            with z.open(f'{name}.py') as module_file:
                python_code = module_file.read().decode('utf-8')

                # Create a new module dynamically
                module = types.ModuleType(name)
                exec(python_code, module.__dict__)  # Execute the code in the module's namespace

                imported_module = module
        else:
            raise FileNotFoundError(f"{name}.py not found in the zip file.")

    
    # Step 2: Access the 'app' variable from the imported module
    deploy = imported_module.Deploy

    working_dir = s3_path

    app = deploy.options(name=name,ray_actor_options={"num_cpus":1.0,'runtime_env':{"working_dir":working_dir}}).bind()
    # Step 3: Use the 'app' with Ray Serve
    serve.run(app, route_prefix=route_prefix, name=name)
    
    return {"msg":f"deploy {name} sucessfully"}

@app.post('/deploy/composite')
async def deploy_composite(name: str):
    """Read Python module from S3 and import it dynamically."""
    # Use s3fs to read the file directly from S3
    route_prefix = f'/{name}'
    s3_path = f's3://santapong/test_composite/{name}.py'
    
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(s3_path, 'r') as f:
        file_content = f.read()

    # Save the file content to a temporary file
    local_file_path = f'./tmp/{name}.py'
    with open(local_file_path, 'w') as local_file:
        local_file.write(file_content)

    # Import the module dynamically using importlib
    spec = importlib.util.spec_from_file_location(name, local_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    imported_module = module
    
    
    # Step 2: Access the 'app' variable from the imported module
    deploy = imported_module.Deploy

    sub_application = [sub_Deploy.bind() for sub_Deploy in deploy.get('sub')]
    
    main_application = deploy.get('main')
    
    app = main_application[0].options(name=name,ray_actor_options={}).bind(sub_application)
    # Step 3: Use the 'app' with Ray Serve
    serve.run(app, route_prefix=route_prefix, name=name)
    
    return {"msg":f"deploy {name} sucessfully"}
    

@app.delete('/model')
async def delete(name: str):
    serve.delete(name)
    
    local_file_path = f'C:/Users/User/Desktop/Git/rays/tmp/{name}.py'
    
    if os.path.exists(local_file_path):
        os.remove(local_file_path)
    
    return {"msg": f"delete {name} success fully"}

@app.get('/check')
async def check(name: str):
    status = serve.status()
    return { name : status.applications[name]}

@app.get('/models')
async def models():
    status = serve.status()
    return {"msg": status.applications}

if __name__ == '__main__':
    uvicorn.run('main:app', port=8001,reload=True)