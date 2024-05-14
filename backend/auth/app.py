from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sqlengine = create_engine("sqlite:///auth.db")
base = declarative_base()

class User(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    
base.metadata.create_all(sqlengine)

Session = sessionmaker(bind=sqlengine)
session = Session()

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str

# Endpoint to register a new user
# This will put the user in the database with no authentication or anything extra
@app.post("/register")
def register_user(username: str, password: str):
    # This is where you would put the user in the database
    existing_user = session.query(User).filter(User.username == username).first()
    if existing_user is not None:
        return {"message": "User already exists"}
    
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    return {"message": "User created"}

app.include_router(router)