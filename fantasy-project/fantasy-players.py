from enum import Enum
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI
import pandas as pd 

csv_file = "./Draft-rankings-export-2025.csv"

df = pd.read_csv(csv_file)

app = FastAPI()

class Positions(str, Enum):
    wr = "WR"
    rb = "RB"
    qb = "QB"
    te = "TE"
    dst = "DEFST"
    k = "K"

class Player(BaseModel):
    rank: int
    name: str
    position: str
    team: str
    projected_points: float

player_list: list[Player] = []

for index, row in df.iterrows():
    player_list.append(
        Player(
            rank=row["Overall Rank"],
            name=row["Full Name"], 
            position=row["Position"], 
            team=row["Team Abbreviation"], 
            projected_points=row["Projected Points"]
        ))

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

@app.get("/players/{position}")
async def get_position(position: Positions):
    res: List[Player] = []
    for player in player_list:
        if player.position == position:
            res.append(player)
    match position:
        case "WR":
            return {"position": position, "message": "You chose the Wide Receivers", "players": res}
        case "RB":
            return {"position": position, "message": "Running Backs - good choice", "players": res}
        case "QB":
            return {"position": position, "message": "You chose the Quarter Backs", "players": res}
        case "TE":
            return {"position": position, "message": "Tight Ends - good choice", "players": res}
        case _:
            return {"position": position, "message": f"Honestly who cares about {position.value}", "players": res}