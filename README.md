# Number Guess

This is a small project I created to practice using FastAPI and experiment with saving game states in-between requests. 

The goal for the user is to guess a number between 0 and 20000.  After starting the game, the user gets a game_id that is mapped to a "secret_number". The user will POST guesses and get either "higher", "lower", or "correct". 


## Getting Started - Running the game server


#### 1. Install requirements inside of a virtual environment:

    pip install fastapi

    pip install "uvicorn[standard]"


#### 2. Run either of the commands to start the server:

    uvicorn main:app --reload

or 

    python app/main.py

 
  
## Getting Started - Playing Number Guess 

This will only work if the game is being hosted on your own home network.  If the game is being hosted outside of development, the url endings will be the same but the website itself won't be http://127:0.0.1:8000/


### 1. Install requests inside of another virtual environment

    pip install requests

### 2. Inside of the python terminal import requests and start a game by entering the following code: 

** Where it says "username" you will select your own username for the game. 

    import requests

    new_game = requests.get("http://127.0.0.1:8000/start/username")
    new_game.json()

    {"game_id": game_id}


The returned game_id will be an integer value used to access your game when you 
you make guesses. 

### 3. Create a python dictionary to store your guess payload.  
This is going to be to body of your post request and includes your unique game_id and the number you want to guess. 

    
    my_guess = {"game_id": <your unique game id>, "guess": 10000}


### 4. Send the guess as a POST request
    url = "http://127.0.0.1:8000/guess/"
    response = requests.post(url, json=my_guess)
    response.json()

    {"guess": 10000, "response": "higher"}

### 5. Continue sending requests and getting feedback on your guesses until you receive the "correct" response

    {"guess": 18013, "response": "correct"}

At this point, the game will end and sending anymore guesses with your game_id will result in an error message. 






