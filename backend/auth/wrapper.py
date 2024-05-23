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
        host=get_env_variable("POSTGRES_HOST"),
        port=5432, 
        database=get_env_variable("POSTGRES_DB"),
    )

def make_session():
    sqlengine = create_engine(get_url(), echo=True)
    Session = sessionmaker(bind=sqlengine)
    session = Session()
    return session

def create_user(username: str, password: str):
    session = make_session()
    existing_user = session.query(UserModel).filter(UserModel.username == username).first()
    if existing_user is not None:
        raise Exception("User already exists")
    
    user = UserModel(username=username, password=password)
    session.add(user)
    session.commit()
    return {"message": "User created"}

def user_login(username: str, password: str):
    session = make_session()
    user = session.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise Exception("User not found")
    if user.password != password:
        raise Exception("Invalid password")
    return {"message": "Login successful"}

def find_user(username: str):
    session = make_session()
    user = session.query(UserModel).filter(UserModel.username == username).first()
    if user is None:
        raise Exception("User not found")
    return {"id": user.id, "username": user.username}

def get_users():
    session = make_session()
    users = session.query(UserModel).all()
    return [{"id": user.id, "username": user.username} for user in users]

