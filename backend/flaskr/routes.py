"""Application routes."""
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import current_app as app
import random

from .models import Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    if selection is None:
        abort(404)

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


@app.after_request
def after_request(response):
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS"
    )
    return response


@app.route("/categories", methods=["GET"])
def get_categories():

    try:
        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[category.id] = category.type
        return jsonify({"seccess": True, "categories": formatted_categories})

    except:
        abort(422)


@app.route("/questions", methods=["GET"])
def get_questions():

    try:
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        categories = Category.query.all()
        formatted_categories = {}
        for category in categories:
            formatted_categories[category.id] = category.type

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "seccess": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": None,
                "categories": formatted_categories,
            }
        )

    except:
        abort(422)


@app.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):

    try:
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "seccess": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(questions),
            }
        )

    except:
        abort(422)


@app.route("/questions", methods=["POST"])
def create_question():
    body = request.get_json()

    search_term = body.get("searchTerm")
    if search_term:
        return search_questions(search_term)

    else:
        for key in ["question", "answer", "category", "difficulty"]:
            if not body or body[key] == None or body[key] == "":
                abort(422)

        new_question = body.get("question", None)
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)

        try:
            question = Question(
                question=new_question,
                answer=answer,
                category=category,
                difficulty=difficulty,
            )
            question.insert()

            questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, questions)

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(questions),
                }
            )

        except:
            abort(422)


def search_questions(search_term):
    questions = []
    try:
        search_query = "%{}%".format(search_term)
        search_results = Question.query.filter(
            Question.question.ilike(search_query)
        ).all()

        for result in search_results:
            questions.append(result)

        current_questions = paginate_questions(request, questions)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
            }
        )

    except:
        abort(422)


@app.route("/categories/<int:category_id>/questions", methods=["GET"])
def questions_by_category(category_id):
    try:

        current_category = Category.query.filter(
            Category.id == category_id
        ).one_or_none()

        questions = Question.query.filter(Question.category == category_id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0 or current_category is None:
            abort(404)

        return jsonify(
            {
                "seccess": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": current_category.type.format(),
            }
        )

    except:
        abort(404)


"""
@TODO: 
Create a POST endpoint to get questions to play the quiz. 
This endpoint should take category and previous question parameters 
and return a random questions within the given category, 
if provided, and that is not one of the previous questions. 

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not. 
"""

"""
@TODO: 
Create error handlers for all expected errors 
including 404 and 422. 
"""


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}), 404


@app.errorhandler(422)
def not_found(error):
    return jsonify({"success": False, "error": 422, "message": "Not found"}), 422
