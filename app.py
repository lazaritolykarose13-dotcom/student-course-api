"""
STUDENT COURSE API
==================
Laboratory Activity 3A - Backend Development Project

A read-only REST API built with Python and Flask.
It serves fictional university courses that are stored directly in this file.
There is no database, no authentication, and no create / update / delete.

Run locally:
    python app.py                        ->  http://127.0.0.1:5000

Run in production on Render:
    gunicorn app:app
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS

# ---------------------------------------------------------------------------
# 1. Create the Flask application object
#    Gunicorn looks for this exact name:
#        gunicorn app:app   ->   file "app.py", object "app"
# ---------------------------------------------------------------------------
app = Flask(__name__)

# CORS: the API is public and read-only, so a classroom demo page is allowed
# to call it from any origin. Replace "*" with your own site later if you like.
CORS(app, resources={r"/api/*": {"origins": "*"}})


# ---------------------------------------------------------------------------
# 2. Sample course records (fictional data stored in code - no database)
# ---------------------------------------------------------------------------
COURSES = [
    {
        "id": 1,
        "code": "CS 101",
        "name": "Introduction to Programming",
        "units": 3,
        "description": "Build your first programs with variables, loops, and functions in Python.",
    },
    {
        "id": 2,
        "code": "IT 204",
        "name": "Database Management Systems",
        "units": 3,
        "description": "Design tables, write SQL queries, and normalize a small school database.",
    },
    {
        "id": 3,
        "code": "IS 310",
        "name": "Systems Integration and Architecture",
        "units": 3,
        "description": "Connect separate services and compare API styles such as REST and SOAP.",
    },
    {
        "id": 4,
        "code": "CS 215",
        "name": "Data Structures and Algorithms",
        "units": 4,
        "description": "Use lists, stacks, queues, trees, and sorting to solve small problems well.",
    },
    {
        "id": 5,
        "code": "NET 150",
        "name": "Computer Networks Fundamentals",
        "units": 3,
        "description": "Explore IP addressing, routing, and how HTTP requests travel to a server.",
    },
    {
        "id": 6,
        "code": "SE 320",
        "name": "Software Engineering Principles",
        "units": 3,
        "description": "Practice requirements gathering, testing, and version control in a team.",
    },
]


# ---------------------------------------------------------------------------
# 3. Required API endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health_check():
    """A. Health Check API - proves the server is running."""
    return jsonify({
        "status": "success",
        "message": "Student Course API is running",
    }), 200


@app.get("/api/courses")
def get_courses():
    """B. Course Collection API - every available course."""
    return jsonify(COURSES), 200


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    """C. Individual Course API - one course, or 404 when it does not exist."""
    for course in COURSES:
        if course["id"] == course_id:
            return jsonify(course), 200

    return jsonify({
        "status": "error",
        "message": "Course with ID " + str(course_id) + " was not found.",
        "available_ids": [course["id"] for course in COURSES],
    }), 404


# ---------------------------------------------------------------------------
# 4. Basic error handling - every error answers in valid JSON
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({
        "status": "error",
        "message": "The requested API route does not exist.",
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    return jsonify({
        "status": "error",
        "message": "This API is read-only. Only GET requests are allowed.",
    }), 405


@app.errorhandler(500)
def handle_server_error(error):
    return jsonify({
        "status": "error",
        "message": "An unexpected server error occurred.",
    }), 500


# ---------------------------------------------------------------------------
# 5. Server configuration
#    Render gives the application a PORT environment variable, so read it.
#    host="0.0.0.0" lets traffic reach the container from outside.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
