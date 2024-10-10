import uvicorn
import importlib.util
import s3fs

import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import UJSONResponse

from utils import SessionDB, import_modules_from_zip_s3, update_file_in_zip_on_s3
from schema.database.base import Model
from schema.api.basemodel import ConfigResourceRay

from config import LOGGING_FORMAT, SQLALCHEMY_URL, S3_BUCKET

import ray
from ray import serve
from ray.runtime_env import RuntimeEnv

from dotenv import load_dotenv
load_dotenv()

# Logging Getter
logging.getLogger(__name__)
logging.Formatter()

# Init Connection
app = FastAPI(default_response_class=UJSONResponse)
session = SessionDB()
s3 = s3fs.S3FileSystem(anon=False)

# App for FastAPI Zone
@app.get('/models')
async def getmodels():
    datas = session.getdata(Model)
    return {"msg": datas}
    



@app.get('/model/name')
async def getmodel_name(model_name: str):
    datas = session.getdata_by_condition(Model, model_name=model_name)
    return {"msg":datas}



# TODO: Make more Adjust Parameter
@app.post('/test_deploy')
async def test_deploy(model_name: str, version: int, route_prefix: str, working_dir: str, runtime_env: str, file: UploadFile=File(None)):
    
    # Check file extension
    if not file.filename.endswith('.zip'):
        return UJSONResponse(content={"error": "File is not a zip file"}, status_code=400)
    
    content = await file.read()
    
    # Save the uploaded file
    s3_path = f's3://santapong/test_zip/{file.filename}'
    with s3.open(s3_path, "wb") as f:
        f.write(content)
    
    loaded_modules = import_modules_from_zip_s3(bucket_name='santapong', zip_key='test_zip/model_1.zip', s3=s3)
    custom_module = loaded_modules[model_name]
    
    # prepare for deploy an specify Application
    deploy = custom_module.Deploy
    
    runtime_env = RuntimeEnv(working_dir=working_dir)
    
    # Application for deploy
    app = deploy.options(name=model_name, ray_actor_options={"num_cpus":1.0,"runtime_env":runtime_env}).bind()
    
    # Deploy Specify Model
    serve.run(app, route_prefix=route_prefix, name=model_name)
    
    # Save deployment to Database
    deployment = {"name": deploy.name}

    # Insert Data to Database Table "Model"
    session.insert_model(model_name=model_name, 
                         version=version, 
                         route_prefix=route_prefix, 
                         working_dir=working_dir, 
                         runtime_env=runtime_env,
                         deployment=deployment)

    return UJSONResponse(content={"filename": file.filename, "name": deploy.name}, status_code=200)
    



@app.post('/deploy')
async def deploy(model_name: str, version: int, route_prefix: str, working_dir: str, runtime_env: str):
    """Read Python module from S3 and import it dynamically."""
    # Use s3fs to read the file directly from S3
    route_prefix = f'/{model_name}'
    s3_path = f's3://santapong/test_zip/{model_name}.py'
    
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(s3_path, 'r') as f:
        file_content = f.read()

    # Save the file content to a temporary file
    local_file_path = f'/tmp/{model_name}.py'
    with open(local_file_path, 'w') as local_file:
        local_file.write(file_content)

    # Import the module dynamically using importlib
    spec = importlib.util.spec_from_file_location(model_name, local_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    imported_module = module
    
    # Step 2: Access the 'app' variable from the imported module
    deploy = imported_module.Deploy

    working_dir = s3_path
    runtime_env = RuntimeEnv(pip=['emoji==2.13.2'],working_dir=working_dir)

    app = deploy.options(name=model_name,ray_actor_options={"num_cpus":1.0,"runtime_env":runtime_env}).bind()
    # Step 3: Use the 'app' with Ray Serve
    serve.run(app, route_prefix=route_prefix, name=model_name)
    
    return {"msg":f"deploy {model_name} sucessfully"}




# TODO: Create Update Model API
@app.patch('/model')
async def updateModel():
    pass




# TODO: Create API for infer Data from Ray API
@app.post('infer')
async def inference():
    return




# TODO: Make health check more flexible
@app.get('/check_health')
async def check_health(model_name: str=None):
        status = serve.status()
        applications = status.applications
        return { "msg" : applications }




# TODO: Make it can Delete on Database
@app.delete('/model')
async def deleteModel(model_name: str):

    serve.delete(model_name)

    return {"msg":f"Remove {model_name} Successfully"}


# TODO: Make it can Modify Model on Database and S3
@app.patch('/model')
async def modifyModel(model: str):
    pass


# Use for Test Upload Zip file to S3
@app.post("/uploadzip/")
async def upload_zip(file: UploadFile = File(...)):
    # Check file extension
    if not file.filename.endswith('.zip'):
        return UJSONResponse(content={"error": "File is not a zip file"}, status_code=400)

    content = await file.read()
    
    # Save the uploaded file
    s3_path = f's3://santapong/test_zip/{file.filename}'
    with s3.open(s3_path, "wb") as f:
        f.write(content)

    return UJSONResponse(content={"filename": file.filename}, status_code=200)

if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8001, reload=True)