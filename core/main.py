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
# Adjust For Resource of Runtime_env
@app.post('/register')
async def register(model_name: str, version: int, route_prefix: str, working_dir: str, runtime_env: str, file: UploadFile=File(None)):
    
    # Check file extension
    if not file.filename.endswith('.zip'):
        return UJSONResponse(content={"error": "File is not a zip file"}, status_code=400)
    
    content = await file.read()
    
    # Save the uploaded file
    s3_path = f's3://santapong/test_zip/{file.filename}'
    with s3.open(s3_path, "wb") as f:
        f.write(content)
    
    loaded_modules = import_modules_from_zip_s3(bucket_name='santapong', zip_key=f'test_zip/{model_name}.zip', s3=s3)
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
    

##### deprecated >> Change to Register
# @app.post('/deploy')


# TODO: Create API for infer Data from Ray API
# POC do it have a way to update api on ray dashboard.
@app.post('/infer/{model_id}')
async def inference(model_id: int):
    return




# TODO: Make health check more flexible
# Not priority.
@app.get('/check_health')
async def check_health(model_name: str=None):
        status = serve.status()
        applications = status.applications
        return { "msg" : applications }



# TODO: Make it can Delete on Database.
@app.delete('/model')
async def deleteModel(model_name: str):

    serve.delete(model_name)
#   session.delete_model() << Make it can delete

    return {"msg":f"Remove {model_name} Successfully"}


# TODO: Make it can Modify Model on Database and S3
@app.patch('/model')
async def modifyModel(model: str):

#   session.update_model() << make it can update model from API.
    
    pass

## Not use from now
# Use for Test Upload Zip file to S3
# @app.post("/uploadzip/")


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8001, reload=True)