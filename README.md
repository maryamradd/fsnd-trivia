# Full Stack Trivia

This trivia app allows you to: 

* Display questions from the database 
* Add new questions
* Search for questions based on a text query string
* Play the quiz game, randomizing either all questions or within a specific category.



## About the Stack

The [backend](./backend) is a Flask and SQLAlchemy server. The [frontend](./frontend) directory contains a React frontend to consume the data from the Flask server through the API, to know more about the API check the backend [readme](./backend/README.md).


## Installation and Usage

this project uses [python3](https://www.python.org/downloads/), [pip](https://pypi.org/project/pip/), [node](https://nodejs.org/) and [npm](https://www.npmjs.com/) so make sure they are installed before proceeding.

#### backend

from the backend directory replace the values in `.env.example` with your values and rename the file to `.env`

install the requirments and start the server:

```sh
$ pip3 install -r requirements.txt
$ flask run
```

#### frontend

install project dependencies and run the app in development mode

```sh
$ npm install 
$ npm start
```


