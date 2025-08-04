from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"Error": "Invalid Request", "details": exc.errors()}
    )

class Worker(BaseModel):
    name: str
    age: int
    role: str

class WorkerAlreadyExists(Exception):
    def __init__(self, name):
        self.name = name

@app.exception_handler(WorkerAlreadyExists)
async def worker_exists_validator(request: Request, exc: WorkerAlreadyExists):
    return JSONResponse(
        status_code=409,
        content={"Error": f"Worker named {exc.name} already exists."}
    )

@app.post("/worker")
def add_worker(worker: Worker):
    if worker.name.lower() == "john":
        raise WorkerAlreadyExists(worker.name)
    return {"Error": f"{worker.name} is a {worker.role.value}"}