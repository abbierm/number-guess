from fastapi import FastAPI
import random
from pydantic import BaseModel
import uvicorn
import os
from pathlib import Path
import logging
from time import strftime
from contextlib import asynccontextmanager


# TODO: Add games to RUNNING_GAMES
# TODO: Intermittently clean up GAMES cache
# TODO: Testing

def add_logging():
    here = os.path.abspath(os.path.dirname(__file__))
    now = strftime("%m_%d_%Y_%h")
    path = Path(here, 'logs', now)
    os.mkdir = path
    logging.basicConfig(filename=path, encoding='utf-8', \
                        level=logging.DEBUG, format='%(asctime)s %(message)s')
    return    


# ===============================================================
# Pydantic Models 
# ===============================================================

class Guess(BaseModel):
    game_id: int
    guess: int

class Response(BaseModel):
    guess: int
    response: str


# ==============================================================
# In-Memory Cache
# ==============================================================

GAMES = {
    0 : {
        "secret_number": 0,
        "username": 'sample',
        "guesses": [],
        "status": True
    },
}


RUNNING_GAMES = {
    # game_id: start-time
}


def log_running_games():
    """Logs unfinished games when server shuts down. """

    logging.info('UNFINISHED GAMES')
    for game_id, time in RUNNING_GAMES.items():
        
        secret_number = GAMES[game_id]["secret_number"]
        username = GAMES[game_id]["username"]
        guesses = GAMES[game_id]["guesses"]
        
        logging.info('game id: %(game_id)s, username: %(username)s secret_number: %(secret_number)s')
        logging.info('guesses: %(guesses)s')
    return 


# ===============================================================
# App + Lifespan Events
# ===============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    add_logging()
    yield
    logging.info('Server is shutting down')
    log_running_games()


app = FastAPI(lifespan=lifespan)

# ===============================================================
#  Game Functions
# ===============================================================

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


# ===============================================================
# API Routes
# ===============================================================


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
    logging.info(f'New Game: {GAMES[new_game_id]}')
    return {"game_id": new_game_id}


@app.post("/guess/")
async def make_guess(guess: Guess):
    if not check_id(guess.game_id):
        logging.debug(f'game not found:  {guess.game_id}')
        return {"error": "game id not found"}
    response = check_number(guess.guess, guess.game_id)
    guess_dict = {guess.guess: response}
    GAMES[guess.game_id]["guesses"].append(guess_dict)
    if response == 'correct':
        logging.info(f"Post Game Results: {GAMES[guess.game_id]}")
        GAMES[guess.game_id]["status"] = False
        return {
            "last_guess": guess.guess,
            "response": response
            }
    else:
        return {"last_guess": guess.guess, "response": response}



def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level='info')
    
      
if __name__ == "__main__":
    main()