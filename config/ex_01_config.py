import ray
from ray import serve
from ray.serve.schema import LoggingConfig

from dotenv import load_dotenv

load_dotenv()

logging_config = LoggingConfig(log_level="DEBUG",logs_dir="/home/santapong/logs/")

@serve.deployment
class model_1:
    def __init__(self):
        return "Hello"
    
app = model_1.options(name='configable_model').bind()

serve.run(app, route_prefix='/config', name='config', logging_config=logging_config)