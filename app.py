from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import oracledb

app = Flask(
    __name__,
    static_folder="D:/Data_X_Pl_sql/Frontend",
    static_url_path=""
)

CORS(app)

connection = oracledb.connect(
    user="SYSTEM",
    password="1313",
    dsn="localhost:1521/XE"
)

@app.route("/")
def home():
    return send_from_directory(
        "D:/Data_X_Pl_sql/Frontend",
        "index.html"
    )


@app.route("/students")
def get_students():
    cursor = connection.cursor()

    cursor.execute("""
        SELECT student_id, student_name, department, marks
        FROM students
        ORDER BY student_id
    """)

    students = []

    for row in cursor:
        students.append({
            "id": row[0],
            "name": row[1],
            "department": row[2],
            "marks": row[3]
        })

    cursor.close()

    return jsonify(students)


@app.route("/add", methods=["POST"])
def add_student():
    data = request.json

    cursor = connection.cursor()

    cursor.callproc(
        "add_student",
        [
            int(data["id"]),
            data["name"],
            data["department"],
            int(data["marks"])
        ]
    )

    cursor.close()

    return jsonify({"message": "Student added successfully"})


@app.route("/update", methods=["PUT"])
def update_student():
    data = request.json

    cursor = connection.cursor()

    cursor.callproc(
        "update_student",
        [
            int(data["id"]),
            data["name"],
            data["department"],
            int(data["marks"])
        ]
    )

    cursor.close()

    return jsonify({"message": "Student updated successfully"})


@app.route("/delete/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    cursor = connection.cursor()

    cursor.callproc(
        "delete_student",
        [student_id]
    )

    cursor.close()

    return jsonify({"message": "Student deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)