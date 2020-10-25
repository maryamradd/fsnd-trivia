# Trivia API

## Getting started

### Installing Dependencies

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 


### Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```
psql trivia < trivia.psql
```

### Enviroment Setup

To setup the enviroment values replace the values in `.env.example` with your values and rename the file to `.env`

the only variable you must change to start the app is the `DATABASE_URI`:
```
DATABASE_URI = postgresql://[USER]:[PASSWORD]@localhost:5432/trivia
```

### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```
flask run
```


## API Reference

### Setup

Base URL: the api runs locally at port 5000. with the base URL is http://localhost:5000/


### Error Handling 

Errors are returned as json objects in the following format:


The error types that the API returns:
- 400: `Bad Request`
- 404: `Not Found`
- 422: `Unprocessable Entity`
- 405: `Method Not Allowed`
- 500: `Internal Server Error`


### Endpoints

#### GET /questions

- returns the list of questions along with a list of categories
- result are paginated with 10 questions per page

Parameters:

- page number: an optional query string parameter for specifing a page number, returns 10 questions for the specified page.


Example: `curl http://localhost:5000/questions`

Response: 

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ], 
  "success": true, 
  "total_questions": 21
}
```


#### GET /categories

- returns a list of available question categories


Example: `curl http://localhost:5000/categories`

Response: 

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
}
```

#### GET /categories/<int:category_id>/questions

- returns the list of questions for the specified category

Parameters:

- category id: a required url path parameter for specifing the id of the category, id should be an integer


Example: `curl http://localhost:5000/categories/2/questions`

Response: 

```
{
    "current_category": "Geography",
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "total_questions": 3
}
```

#### POST /questions

- can be used as a search query or for creating a new question based of the body of the request

##### Searching questions 

Request Body:

- a json object with the search term

Request body example:
```
{
    "searchTerm": "largest"

}
```

Example: `curl -X POST http://localhost:5000/questions`

Response: 

```
{
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```

##### Creating new questions

- a json object specifing the details of the question to be created:
    - `question`: (string) question in string format
    - `answer`: (string) answer for the question
    - `category`: (int) category of the question 
    - `difficulty`: (int) difficulty of question on scale form 1 to 5

Request body example:

```
{   
    "question": "Why are flamingos pink?",
    "answer": "From eating shrimp",
    "category": 1,
    "difficulty": 1
}
```


Example: `curl -X POST http://localhost:5000/questions`

Response:    

```
{
    "created": 41,
    "questions": [
        .......................
    ],
    "success": true,
    "total_questions": 21
}
```

#### DELETE /questions/<int:question_id>

- deletes the question with the specified id

Parameters:

- question id: a required url path parameter for specifing the id of the question to be deleted, id should be an integer


Example: `curl -X DELETE http://localhost:5000/questions/4`

Response: 

```
{
    "deleted": 4,
    "questions": [
       ..............
    ],
    "success": true,
    "total_questions": 20
}
```

#### POST /quizzes

- used for playing the quiz game, returns a random question that is not in the previous_questions list based on a specified category (or all).

Request Body:

- a json object that contains:
    - `previous_questions`: (array) a list of id's of the previous questions (empty at the start of the game).
    - `quiz_category`: (json object) a key-value pair that contains the quiz category id and  the category type.
        - `id`: (int) the category id (`0` is to get questions from all categories)
        - `type`: (string) optional category name
 
Request body example:
```
{   
    "previous_questions": [13, 9],
    "quiz_category": {
        "type": "Science",
        "id":1
    }
}
```

Example: `curl -X POST http://localhost:5000/quizzes`

Response: 

```
{
    "question": {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
    },
    "success": true
}
```



### Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```