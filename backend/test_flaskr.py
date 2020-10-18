from os import environ
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from flaskr import create_app, db
from flaskr.models import Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["DEBUG"] = False
        self.app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("TEST_DATABASE_URI")

        self.client = self.app.test_client

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        # self.app_context.pop()

    def test_get_paginated_questions(self):
        """
        tests getting all questions with pagination
        """

        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()