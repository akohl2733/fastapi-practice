from pydantic import BaseModel, Field
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class Role(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class Address(BaseModel):
    street: str
    number: int
    city: str
    zip_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address

class Worker(BaseModel):
    name: str
    role: Role

class Student(BaseModel):
    full_name: str = Field(..., alias="fullname")
    email: str

    class Config:
        allow_population_by_field_name = True

@app.post("/user")
async def create_user(user: User):
    return {"Msg": f"{user.name} lives in {user.address.city}"}

@app.post("/worker")
async def create_worker(worker: Worker):
    return {"Msg": f"{worker.name} is a {worker.role.value}"}