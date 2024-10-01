import s3fs
import importlib.util
import os

import ray
from ray import serve

from dotenv import load_dotenv

load_dotenv()


def import_module_from_s3(bucket_name, s3_key, module_name):
    """Read Python module from S3 and import it dynamically."""
    # Use s3fs to read the file directly from S3
    s3 = s3fs.S3FileSystem(anon=False)
    with s3.open(f's3://{bucket_name}/{s3_key}', 'r') as f:
        file_content = f.read()

    # Save the file content to a temporary file
    local_file_path = f'C:/Users/User/Desktop/Git/rays/tmp/{module_name}.py'
    with open(local_file_path, 'w') as local_file:
        local_file.write(file_content)

    # Import the module dynamically using importlib
    spec = importlib.util.spec_from_file_location(module_name, local_file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Define your S3 bucket and file key
bucket_name = 'santapong'
s3_key = 'test/ex_05_deploy/ex_04_deploy_mulitple_request.py'  # Python file on S3
module_name = 'your_module'  # Module name for import

# Step 1: Import the module from S3
imported_module = import_module_from_s3(bucket_name, s3_key, module_name)

# Step 2: Access the 'app' variable from the imported module
app = imported_module.app

# Step 3: Use the 'app' with Ray Serve
serve.run(app, route_prefix='/Ingresss', name='Ingresss')