import ray
from ray import serve

from dotenv import load_dotenv
import s3fs
import types

load_dotenv()



def import_module_from_s3(bucket_name, key):
    # Initialize S3 filesystem
    s3 = s3fs.S3FileSystem(anon=False)
    
    # Read the Python file content from S3
    with s3.open(f'{bucket_name}/{key}', 'r') as file:
        python_code = file.read()

    # Create a new module dynamically
    module = types.ModuleType(key.split('/')[-1].split('.')[0])  # module name without extension
    exec(python_code, module.__dict__)  # Execute the code within the module's namespace

    return module

# Example usage
bucket_name = 'santapong'
key = 'test/model_8.py'
custom_module = import_module_from_s3(bucket_name, key)

# Now you can use functions and classes from the module
Deploy = custom_module.Deploy

app = Deploy.options(name='model_10').bind()

serve.run(app, route_prefix='/model_8', name='model_8')