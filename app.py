from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flasgger import Swagger

app = Flask(__name__)

# Replace with your SQL Server connection details
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SA:vijay123@FINFLOCK2\\SQLEXPRESS/student?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SA:vijay123@host.docker.internal/student?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Flasgger configuration
app.config['SWAGGER'] = {
    'swagger': '2.0',
    'title': 'Student API',
    'uiversion': 3,
    'specs_route': '/apidocs/'  # Specify the custom route
}

swagger = Swagger(app)

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
    try:
        sql = text("SELECT * FROM students")
        result = db.session.execute(sql)
        
        # Handle case where result is None
        if not result:
            return jsonify({"message": "No data found in the students table"}), 404
        
        # Get column names
        columns = result.keys()

        # Convert each row into a dictionary
        students = [dict(zip(columns, row)) for row in result]
        
        return jsonify(students)
    
    except Exception as e:
        # Catch and log any errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
