import os, sys
sys.path.append(os.path.join(os.getcwd(),"core"))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from schema.database.base import Base, Model

from config import SQLALCHEMY_URL



class ConnectDatabase:
    pass

class CreateSession:
    def __init__(self, database_url: str, base: any):
        self.engine = create_engine(database_url)
        self.session = sessionmaker(bind=self.engine)()

    def create_table(self):
        Base.metadata.create_all(bind=self.engine)
    
    def getdata(self, Table):
        return self.session.query(Table).all()
        
    def __example(self):
        pass

if __name__ == '__main__':
    Session = CreateSession(SQLALCHEMY_URL, Base)
    Session.create_table()
    data = Session.getdata(Table=Model)

    print(data)