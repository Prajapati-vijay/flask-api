from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flasgger import Swagger
from flask import redirect

app = Flask(__name__)

# Replace with your SQL Server connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SA:vijay123@doker.host.internal/student?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Set Swagger UI URL to root `/`
app.config['SWAGGER'] = {
    'uiversion': 3,
    'openapi': '3.0.2'
}
swagger = Swagger(app)



@app.route('/')
def index():
    return redirect('/apidocs')


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
    app.run(debug=True)    
