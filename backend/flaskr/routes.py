"""Application routes"""
import os, sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
from flask import current_app as app
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
        return jsonify({"success": True, "categories": formatted_categories})

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
                "success": True,
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
                "success": True,
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

    # if the body containts a search term execute the search function
    # otherwise continue with creating a new question
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
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "current_category": current_category.type.format(),
            }
        )

    except:
        abort(404)


@app.route("/quizzes", methods=["POST"])
def random_quiz_question():
    body = request.get_json()
    try:
        category = body.get("quiz_category")
        prev_questions = body.get("previous_questions")

        if not body or category is None or prev_questions is None:
            abort(400)

        # if category id is 0 query the database for questions from all categories
        # otherwise query the database for questions from the selected category

        if category["id"] == 0:
            category_questions = Question.query.order_by(func.random())

        else:
            category_questions = Question.query.filter(
                Question.category == category["id"]
            ).order_by(func.random())

        # select a question that is not in the previous questions list
        new_question = category_questions.filter(
            Question.id.notin_(prev_questions)
        ).first()

        if new_question is None:
            # no more questions to be played
            return jsonify({"success": True})

        return jsonify({"success": True, "question": new_question.format()})

    except:
        abort(422)


"""Error handlers"""


@app.errorhandler(400)
def not_found(error):
    return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not Found"}), 404


@app.errorhandler(422)
def not_found(error):
    return (
        jsonify({"success": False, "error": 422, "message": "Unprocessable Entity"}),
        422,
    )
