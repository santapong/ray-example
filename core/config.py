import os

from dotenv import load_dotenv
load_dotenv()

# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

#SQLALCHEMY_URL = 'postgresql://postgres:Jobbullet7475@localhost:5432/test_ray'
SQLALCHEMY_URL = 'sqlite:///E:\\Repository\\ray-example\\database\\data.db'

S3_BUCKET = 'santapong'
S3_PREFIX = ''

# Default Log Format 
LOGGING_FORMAT = ''

# Log config
LOGGINE_LEVEL = ''

RAY_DASHBOARD_URL = 'http://192.168.232.208:8265'