from fastapi import FastAPI
import random
from pydantic import BaseModel
import uvicorn



# TODO: Add Logging
# figure out when to log or clear the in memory database
# Once user completes 
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")


class Guess(BaseModel):
    game_id: int
    guess: int


class Response(BaseModel):
    guess: int
    response: str



app = FastAPI()


GAMES = {
    0 : {
        "secret_number": 0,
        "username": 'sample',
        "guesses": [],
        "status": True
    },
}

# TODO: Logging results to a file



def pick_number() -> int:
    return random.randint(0, 999)

def check_id(game_id: int) -> bool:
    try:
        x = GAMES[game_id]["status"]
        if x is True:
            return True
        else:
            return False
    except(KeyError):
        return False

def check_number(number: int, game_id: int) -> str:
    secret_number = GAMES[game_id]["secret_number"]
    if number == secret_number:
        return 'correct'
    elif number > secret_number:
        return 'lower'
    else:
        return 'higher'


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/start/{username}")
def start_game(username: str):
    new_game_id = max(GAMES) + 1
    secret_number = pick_number()
    GAMES[new_game_id] = {
        "secret_number": secret_number,
        "username": username,
        "guesses": [],
        "status": True
    }
    return {"game_id": new_game_id}


@app.post("/guess/")
async def make_guess(guess: Guess):
    if not check_id(guess.game_id):
        return {"error": "game id not found"}
    response = check_number(guess.guess, guess.game_id)
    guess_dict = {guess.guess: response}
    GAMES[guess.game_id]["guesses"].append(guess_dict)
    if response == 'correct':
        GAMES[guess.game_id]["status"] = False
        return {
            "last_guess": guess.guess,
            "response": response
            }
    else:
        return {"last_guess": guess.guess, "response": response}


