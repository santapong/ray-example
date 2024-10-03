import s3fs
import zipfile
import io
import sys
import importlib.util
import types

from dotenv import load_dotenv

load_dotenv()

import ray
from ray import serve
from ray.runtime_env import RuntimeEnv

# Function to import a module from in-memory python code
"""
The function `import_modules_from_zip_s3` loads Python modules from a .zip file stored in an S3
bucket and allows access to specific modules and their functions.

:param module_name: The `module_name` in the provided code refers to the name of the module you want
to access from the loaded modules. In this case, it is used to specify which module you want to use
from the modules that were loaded from the zip file
:param python_code: The code you provided defines a function `load_module_from_code` that loads a
Python module from in-memory code, and another function `import_modules_from_zip_s3` that imports
modules from a zip file stored in an S3 bucket
:return: The `import_modules_from_zip_s3` function returns a dictionary where the keys are the
module names extracted from the .py files in the zip archive, and the values are the corresponding
module objects loaded into memory using the `load_module_from_code` function.
"""
def load_module_from_code(module_name, python_code):
    # Create a new module object
    module = types.ModuleType(module_name)
    exec(python_code, module.__dict__)
    sys.modules[module_name] = module  # Add to sys.modules for future imports
    return module

def import_modules_from_zip_s3(bucket_name, zip_key):
    # Initialize S3 filesystem
    s3 = s3fs.S3FileSystem(anon=False)

    # Read the .zip file content from S3
    with s3.open(f'{bucket_name}/{zip_key}', 'rb') as s3_file:
        zip_data = s3_file.read()

    # Open the zip file in memory
    with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
        # Extract all .py files from the zip into memory
        python_files = {name: z.read(name).decode('utf-8') for name in z.namelist() if name.endswith('.py')}
        
        modules = {}
        
        # Loop through the extracted python files and load them as modules
        for file_name, code in python_files.items():
            module_name = file_name[:-3].replace('/', '.')  # Convert filename to a proper module name
            
            # Load module into memory
            modules[module_name] = load_module_from_code(module_name, code)

        return modules

# Example usage
bucket_name = 'santapong'
zip_key = 'test_zip/model_1.zip'

# Import all modules from the zip file
loaded_modules = import_modules_from_zip_s3(bucket_name, zip_key)

# Access the specific module and its functions
name = 'model_1'
module_name = 'model_1'  # The module you want to use
custom_module = loaded_modules[module_name]
route_prefix = '/model_1'

# Now you can use functions and classes from the module
deploy = custom_module.Deploy


runtime_env = RuntimeEnv(pip=['numpy==1.26.4'],working_dir='s3://santapong/test_zip/model_1.zip')

app = deploy.options(name=name,ray_actor_options={"num_cpus": 1.0,"runtime_env":runtime_env}).bind()
# Step 3: Use the 'app' with Ray Serve
serve.run(app, route_prefix=route_prefix, name=name)

    