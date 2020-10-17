# Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

this trivia app allows you to: 
    - Display questions from the database 
    - Add new questions
    - Search for questions based on a text query string
    - Play the quiz game, randomizing either all questions or within a specific category.


## About the Stack

The `./backend` directory is a Flask and SQLAlchemy server. The `./frontend` directory contains a complete React frontend to consume the data from the Flask server.


## Installation 

Install the dependencies and requirments:
    - clone the repository
    - in the backend directory replace the values in `.env.example` with your values and rename the file to `.env`
    - install the requirments and start the server

```sh
$ cd backend
$ pip3 install -r requirements.txt
$ flask run
```

    - for the react frontend

```sh
$ cd frontend
$ npm install 
$ npm start
```


