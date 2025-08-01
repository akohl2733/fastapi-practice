from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI()

class TooYoungException(Exception):
    def __init__(self, age: int):
        self.age = age

@app.exception_handler(TooYoungException)
def too_young_handler(request: Request, exc: TooYoungException):
    return JSONResponse(
        status_code=418,
        content={"detail": f"You are {exc.age}. You must be 18 years of age to vote"}
    )

class Feedback(BaseModel):
    message: str
    rating: Optional[int] = Field(None, ge=1, le=10)

class RegisterUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    age: int = Field(..., gt=0, lt=120)

@app.post('/user/')
def register_user(user: RegisterUser):
    return {"success": f"{user.username} is {user.age} years old."}

@app.get("/search")
def search(q: str = Query(..., min_length=3, max_length=20)):
    return {"query": q}

@app.get("/protected")
def read_password(key: str):
    if key != "opensesame":
        raise HTTPException(status_code=403, detail="invalid access key")
    return {"login": "success"}

@app.get("/vote")
def see_if_vote(age: int):
    if age < 18:
        raise TooYoungException(age)
    return {"Success": "You are able to vote"}