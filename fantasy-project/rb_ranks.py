from enum import Enum
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
import pandas as pd 

csv_file = "./rb_totals_v1.csv"

df = pd.read_csv(csv_file)

app = FastAPI()

class Positions(str, Enum):
    wr = "WR"
    rb = "RB"
    qb = "QB"
    te = "TE"
    dst = "DEFST"
    k = "K"

csv_file = "./rb_totals_v1.csv"
df = pd.read_csv(csv_file)

class Player(BaseModel):
    name: str
    total_touches: float
    rush_points: float
    rec_points: float
    total: float
    position_rank: int

player_list: list[Player] = []

for index, row in df.iterrows():
    player_list.append(
        Player(
            name = row["name"],
            total_touches = row["total_touches"],
            rush_points = round(row["rush_points"], 2),
            rec_points = round(row["rec_points"], 2),
            total = round(row["total"], 2),
            position_rank = row["position_rank"]
        )
    )

@app.get('/')
def root():
    return {
        "Fantasy players": "use '/players' route",
        "Players to look for": {
            "wide receivers": "WR",
            "running backs": "RB",
            "quarter backs": "QB"
        }
    }

@app.post('/players')
async def add_player(player: Player):
    player_list.append(player)
    return {"Player added": "Success"}

@app.get("/players")
async def get_players():
    return player_list