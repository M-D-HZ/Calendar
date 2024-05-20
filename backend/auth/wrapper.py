
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from models import UserModel
import os

def get_env_variable(name: str):
    return os.getenv(name, "")

def get_url():
    return URL.create(
        drivername="postgresql+psycopg2",
        username=get_env_variable("POSTGRES_USER"),
        password=get_env_variable("POSTGRES_PASSWORD"),
        host="auth-db",
        port=5432, 
        database=get_env_variable("POSTGRES_DB"),
    )

sqlengine = create_engine(get_url(), echo=True)

Session = sessionmaker(bind=sqlengine)
session = Session()

def create_user(username: str, password: str):
    print(get_url())
    existing_user = session.query(UserModel).filter(UserModel.username == username).first()
    if existing_user is not None:
        return {"message": "User already exists"}
    
    user = UserModel(username=username, password=password)
    session.add(user)
    session.commit()
    return {"message": "User created"}