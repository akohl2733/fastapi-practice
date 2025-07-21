from typing import Annotated, TypeVar
from datetime import datetime, timedelta
from uuid import UUID
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class ZoneLevelRow(BaseModel):
    level_name: str
    mean_occupancy: float | None = None
    capacity: int | None = None

class ZoneLevelOccupancy(BaseModel):
    result: list[ZoneLevelRow]

zone_level_list: list["ZoneLevelRow"] = []

@app.post("/zone/")
def addZone(row: ZoneLevelRow):
    zone_level_list.append(row)
    return {"message": "Zone added!"}

@app.get("/zone/")
def get_zones():
    return zone_level_list