from os import environ
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app, db
from flaskr.models import Question, Category
import unittest


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app("testing")
        self.app_context = self.app.app_context()

        # binds the app to the current context
        self.app_context.push()
        with self.app.test_client():
            self.client = self.app.test_client()

    def tearDown(self):
        # executed after each test to pop the app context
        self.app_context.pop()

    def test_get_paginated_questions(self):
        """
        tests getting all questions with pagination
        """

        response = self.client.get("/api/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)

    def test_fail_paginated_questions(self):
        """
        tests getting a question with an invalid page id
        """

        response = self.client.get("/api/questions?page=999")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_get_categories(self):
        """
        tests getting the list of categories
        """

        response = self.client.get("/api/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("categories", data)

    def test_fail_get_categories(self):
        """
        tests getting a list of categories that doesn't exist on db
        """

        # delete the category table
        Category.query.delete()
        response = self.client.get("/api/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_get_questions_by_category(self):
        """
        tests getting questions from a specified categories
        """

        response = self.client.get("/api/categories/2/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)
        self.assertIn("current_category", data)

    def test_fail_get_questions_by_category(self):
        """
        tests getting questions from a category that doesn't exist
        """

        response = self.client.get("/api/categories/99/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_question_by_id(self):
        """
        tests deleting a question by id
        """

        response = self.client.delete("/api/questions/17")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("deleted", data)
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)

    def test_fail_delete_question_by_id(self):
        """
        tests deleting a question with an invalid id
        """

        response = self.client.delete("/api/questions/999")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_search_question(self):
        """
        tests searching for a question that contains the passed search term
        """

        response = self.client.post("/api/questions",
                                    json={"searchTerm": "title"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)

    def test_fail_search_question(self):
        """
        tests searching for a question with a search term
        that contains special characters
        """

        response = self.client.post("/api/questions",
                                    json={"searchTerm": "'1=1'%&"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_create_question(self):
        """
        tests creating a new question
        """

        response = self.client.post(
            "/api/questions",
            json={
                "question": "Why are flamingos pink?",
                "answer": "From eating shrimp",
                "category": 1,
                "difficulty": 1,
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("created", data)
        self.assertIn("questions", data)
        self.assertIn("total_questions", data)

    def test_fail_create_question(self):
        """
        tests creating a new question with missing
        body arguments (answer, difficulty)
        """

        response = self.client.post(
            "/api/questions",
            json={
                "question": "Why are flamingos pink?",
                "category": 1,
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_retrive_quiz_question(self):
        """
        tests retriving a random quiz question from a
        category that is not in the previous questions
        """

        response = self.client.post(
            "/api/quizzes",
            json={
                "quiz_category": {"type": "Science", "id": 1},
                "previous_questions": [17],
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn("question", data)

    def test_fail_retrive_quiz_question(self):
        """
        tests retriving a quiz question without specifing the category
        """

        response = self.client.post(
            "/api/quizzes",
            json={
                "previous_questions": [16, 10],
            },
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
