import os, sys
sys.path.append(os.path.join(os.getcwd(),"core"))

from token import OP
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from schema.database.base import Base, Model

from config import SQLALCHEMY_URL

import logging
from logging.handlers import RotatingFileHandler

logging.getLogger(__name__)
logging.Formatter()

class ConnectDatabase:
    pass

# TODO: Make it can Delete and Update Data in Database
class SessionDB:
    
    def __init__(self, database_url: str=SQLALCHEMY_URL, base_model: declarative_base=Base):
        self.engine = create_engine(database_url, echo=False)
        self.session = sessionmaker(bind=self.engine)()
        self.base_model = base_model

    def create_table(self):
        self.base_model.metadata.create_all(bind = self.engine)
    
    def getdata(self, Table) -> list:
        return self.session.query(Table).all()
        
    def getdata_by_condition(self, Table: str, model_name: str):
        return self.session.query(Table).filter_by(model_name=model_name).all()    
        
    def __example(self):
        pass
    
    def insert_model(self,  
               model_name: Optional[str],
               route_prefix: Optional[str],
               version: Optional[int],
               working_dir: Optional[str],
               runtime_env: Optional[str],
               **kwargs
               ):
        with self.session as session:
            new_data = Model(model_name=model_name, route_prefix=route_prefix, version=version, working_dir=working_dir, runtime_env= runtime_env)
            session.add(new_data)
            session.commit()

    def update_model(self):
        pass

    def delete_model(self):
        pass

if __name__ == '__main__':
    SessionDB = SessionDB(SQLALCHEMY_URL, Base)
    SessionDB.create_table()
    SessionDB.insert_model(id=2,model_name="test",version='2',route_prefix='/testssss',working_dir='testssss',runtime_env='test')
    
    datas = SessionDB.getdata(Table=Model)
    for data in datas:
        print(f'Model ID:{data.id}, model_name:{data.model_name}, route_prefix:{data.route_prefix}')
        
    condatas = SessionDB.getdata_by_condition(Table=Model,model_name="Hello")
    for condata in condatas:
        print(condata.model_name)