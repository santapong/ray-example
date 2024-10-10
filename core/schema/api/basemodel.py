import os, sys
sys.path.append(os.path.join(os.getcwd(),'core'))

from pydantic import BaseModel

class ConfigResourceRay(BaseModel):
    pass