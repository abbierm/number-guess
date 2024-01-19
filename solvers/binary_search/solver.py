import requests
import math
import argparse


def _parse_arguments() -> dict:
    """
    Returns:
        args: Dictionary of parsed args
        keys: ['username', 'top_value']
    """
    parser = argparse.ArgumentParser(description="Plays a number guessing API game.")

    command_help = "'username' is what you want your username to be and 'top_value' is the highest number that the secret number can be. "

    parser.add_argument('username', default='CorgiLover', help=command_help)
    parser.add_argument('top_value', default=20000, type=int, help=command_help)
    args = parser.parse_args()
    return args


def _start_game(username: str) -> int:
    url = f"http://127.0.0.1:8000/start/{username}"
    response = requests.get(url)
    return response.json()


def _make_guess(game_id: int, guess: int) -> dict:
    x = {"game_id": game_id, "guess": guess}
    url = f"http://127.0.0.1:8000/guess/"
    r = requests.post(url, json=x)
    return r.json()


def choose_guess(game_id: int, top_value: int, guesses=0, upper_bound=None,
                    lower_bound=None):
    if upper_bound is None and lower_bound is None:
        upper_bound, lower_bound = top_value, 0
    if lower_bound > upper_bound:
        return {"guesses": guesses, "secret_number": None}

    mid = math.floor((upper_bound + lower_bound) / 2)

    r = _make_guess(game_id, mid)
    guesses += 1

    if r["response"].lower() == "correct":
        return {"guesses": guesses, "secret_number": mid}
    elif r["response"].lower() == "higher":  
        return choose_guess(game_id, top_value, guesses, upper_bound, mid + 1)
    else:
        return choose_guess(game_id, top_value, guesses, mid - 1, lower_bound)


def run_game_loop(username, top_value):
    r = _start_game(username)
    new_id = r['game_id']
    x = choose_guess(new_id, top_value)
    print(x)
    return x
    

if __name__ == "__main__":
    args = _parse_arguments()
    results = run_game_loop(args.username, args.top_value)
    print(results)