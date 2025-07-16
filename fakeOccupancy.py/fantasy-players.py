from enum import Enum
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI


app = FastAPI()

class Positions(str, Enum):
    wr = "WR"
    rb = "RB"
    qb = "QB"
    te = "TE"
    dst = "DEFST"
    k = "K"

class Player(BaseModel):
    name: str
    position: str
    team_played_for: list[str]

player_list: list[Player] = []

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
    for player in player_list:
        return {player.name: player.team_played_for}

@app.get("/players/{position}")
async def get_position(position: Positions):
    res: List[Player] = []
    for player in player_list:
        if player.position == position:
            res.append(player)
    if position.value == "WR":
        return {"position": position, "message": "You chose the Wide Receivers", "players": res}
    if position is Positions.rb:
        return {"position": position, "message": "Running Backs - good choice", "players": res}
    if position.value == "QB":
        return {"position": position, "message": "You chose the Quarter Backs", "players": res}
    if position is Positions.te:
        return {"position": position, "message": "Tight Ends - good choice", "players": res}
    return {"position": position, "message": f"Honestly who cares about {position.value}", "players": res}