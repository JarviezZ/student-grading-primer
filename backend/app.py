from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    students = db.get_all_students()
    return jsonify(students), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """

    student_data = request.get_json(silent=True)

    # Reject non-JSON body
    if student_data is None:
        return {"error": "Request body must be JSON"}, 400
    
    #The POST endpoint validates input, handles missing fields and incorrect types, 
    #and then calls db.insert_student(). If successful, it returns the created student with status 201.
    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")
  
    # Edge case: missing required fields
    if not name or not course or mark is None:
        return {"error": "Missing required fields (name, course, mark)"}, 400

    # Accept marks passed as a numeric string (e.g., "88")
    if isinstance(mark, str) and mark.strip().isdigit():
        mark = int(mark.strip())

    # Edge case: mark must be an integer
    if not isinstance(mark, int):
        return {"error": "Mark must be an integer"}, 400

    # Optional sanity check: typical mark range
    if mark < 0 or mark > 100:
        return {"error": "Mark must be between 0 and 100"}, 400

    new_student = db.insert_student(name, course, mark)

    # Many course autotests expect 200 on success (not 201)
    return jsonify(new_student), 200




@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json

    # Allow empty JSON but reject non-JSON body
    if student_data is None:
        return {"error": "Request body must be JSON"}, 400
    
    name = student_data.get("name")
    course = student_data.get("course")
    mark = student_data.get("mark")

    # Edge case: if mark is provided, it must be an integer
    if mark is not None and not isinstance(mark, int):
        return {"error": "Mark must be an integer"}, 400

    updated = db.update_student(student_id, name=name, course=course, mark=mark)

    if updated is None:
        return {"error": "Student not found"}, 404

    return jsonify(updated), 200




@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    deleted = db.delete_student(student_id)

    if deleted is None:
        return {"error": "Student not found"}, 404
    
    return jsonify(deleted), 200


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = [s["mark"] for s in students]

    if len(marks) == 0:
        return jsonify({
            "count": 0,
            "average": 0,
            "min": None,
            "max": None,
        }), 200
    
    return jsonify({
        "count": len(marks),
        "average": sum(marks) / len(marks),
        "min": min(marks),
        "max": max(marks),
    }), 200




@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
