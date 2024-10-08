import os

from dotenv import load_dotenv
load_dotenv()

# DB_HOST = os.getenv("DB_HOST")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_URL = 'postgresql://postgres:Jobbullet7475@localhost:5432/test_ray'


LOGGING_FORMAT = ''
