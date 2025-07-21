from pydantic import BaseModel
from fastapi import FastAPI
import typing

app = FastAPI()

class ZoneLevel(BaseModel):
    zone_name: str
    mean_occupancy: float
    capacity: int

class ZoneLevelOccupancy(BaseModel):
    results: list[ZoneLevel]

zone_level_list: list[ZoneLevel] = []

@app.post("/zone/")
def add_zone(row: ZoneLevel):
    zone_level_list.append(row)
    return {"Success": "Was added to list"}

@app.get("/zone/")
def get_zones():
    return zone_level_list