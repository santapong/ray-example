import os, sys

sys.path.append(os.path.join(os.getcwd(),'core'))
# print(sys.path)

import logging 
from logging.handlers import RotatingFileHandler

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Engine, create_engine, Column, Integer, String, inspect, JSON

from config import SQLALCHEMY_URL, LOGGING_FORMAT

logging.getLogger(__name__)
logging.Formatter(LOGGING_FORMAT)

# Use to Connect to Database
engine = create_engine(SQLALCHEMY_URL)

# Use for intialize Database Connect
Base = declarative_base()

# Table Model For database
class Model(Base):
    r"""
    Table Model Object
    id int
    model_name str
    version int
    working_dir str
    runtime_env str
    """
    __tablename__ = 'Model'

    id = Column(Integer, primary_key=True)
    model_name = Column(String)
    route_prefix = Column(String, unique=True)
    version = Column(Integer)
    working_dir = Column(String , unique=True)
    runtime_env = Column(JSON)
    deployment = Column(JSON)

# def create_table_if_not_exist(
#         engine: Engine
#         ):
#     inspect = inspect(engine)   
#     if not inspect.has_table(User.__tablename__):   
#             Base.metadata.create_all(engine)        

if __name__ == '__main__':
    
    # Create Database
    Base.metadata.create_all(engine)

    # Session = sessionmaker(bind=engine)
    
    # with Session() as session:
    #     new_model = Model(id=1, model_name="Hello", version='1', working_dir='test', runtime_env='test22', route_prefix='/hello')
    #     session.add(new_model)
    #     session.commit()

    #     models = session.query(Model).all()
    #     for model in models:
    #         print(f'Model ID:{model.id}, model_name:{model.model_name}')