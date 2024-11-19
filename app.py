from flask import Flask, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flasgger import Swagger

app = Flask(__name__)

# Replace with your SQL Server connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SA:vijay123@docker.host.internal/student?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set application root if served behind a reverse proxy with a prefix (e.g., "/flask")
app.config['APPLICATION_ROOT'] = '/flaskapi'

db = SQLAlchemy(app)

# Configure Swagger
swagger = Swagger(app)

@app.route('/')
def index():
    """
    Redirect to the Swagger docs, dynamically handling the base path.
    """
    # Dynamically generate the URL for the Swagger docs
    return redirect(url_for('flasgger.apidocs'))

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

if __name__ == '__main__':
    # Ensure Flask respects the application root when running in Docker
    app.run(debug=True)
