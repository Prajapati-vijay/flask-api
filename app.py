from flask import Flask, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flasgger import Swagger
import os

app = Flask(__name__)

# Replace with your SQL Server connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SA:vijay123@host.docker.internal/student?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Swagger configuration
app.config["SWAGGER"] = {
    "uiversion": 3,
    "openapi": "3.0.2",
    "static_url_path": "/flasgger_static",  # Static files path under /flasgger_static
    "specs_route": "/apidocs",  # Swagger UI route under /apidocs
}
swagger = Swagger(app)

# Define a custom static path for Swagger UI if needed
@app.route("/flasgger_static/<path:filename>")
def custom_swagger_static(filename):
    return app.send_static_file(f"./swaggerui/{filename}")   

# @app.route('/')
# def index():
#     # Redirect to Swagger UI docs at /apidocs
#     return redirect("/apidocs")

@app.route('/students', methods=['GET'])
def get_students():
    """
    Get all students
    ---
    responses:
      200:
        description: A list of students
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: The student ID
              name:
                type: string
                description: The student's name
              age:
                type: integer
                description: The student's age
    """
    sql = text("SELECT * FROM students")
    result = db.session.execute(sql)
    
    # Get column names
    columns = result.keys()
    
    # Convert each row into a dictionary
    students = [dict(zip(columns, row)) for row in result]
    
    return jsonify(students)

# Custom UI route to serve the Swagger UI with relative paths
@app.route("/apidocs")
def custom_ui():
    return render_template(
        "swagger-ui.html", title="API Documentation", specs_url="./swagger.json"
    )

if __name__ == '__main__':
    app.run(debug=True)
