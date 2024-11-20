# from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import text
# from flasgger import Swagger

# app = Flask(__name__)

# # Replace with your SQL Server connection details
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SA:vijay123@host.docker.internal/student?driver=ODBC+Driver+17+for+SQL+Server'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# # Dynamically set the Swagger configuration based on the prefix
# SWAGGER_URL_PREFIX = '/fastapi'  # Your prefix
# app.config['SWAGGER'] = {
#     'swagger': '2.0',
#     'title': 'Student API',
#     'uiversion': 3,
#     'specs_route': f'{SWAGGER_URL_PREFIX}/apidocs/'  # Use the prefix
# }

# swagger = Swagger(app,static_url_path='/fastapi/flasgger_static')

# @app.route(f'{SWAGGER_URL_PREFIX}/students', methods=['GET'])
# def get_students():
#     """
#     Get all students
#     ---
#     responses:
#       200:
#         description: A list of students
#         schema:
#           type: array
#           items:
#             type: object
#             properties:
#               id:
#                 type: integer
#                 description: The student ID
#               name:
#                 type: string
#                 description: The student's name
#               age:
#                 type: integer
#                 description: The student's age
#     """
#     try:
#         sql = text("SELECT * FROM students")
#         result = db.session.execute(sql)
        
#         # Handle case where result is None
#         if not result:
#             return jsonify({"message": "No data found in the students table"}), 404
        
#         # Get column names
#         columns = result.keys()

#         # Convert each row into a dictionary
#         students = [dict(zip(columns, row)) for row in result]
        
#         return jsonify(students)
    
#     except Exception as e:
#         # Catch and log any errors
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



from flask import Flask, Blueprint
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy

# Configuration
class Config:
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://server_name/database_name?trusted_connection=yes&driver={ODBC Driver 17 for SQL Server}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Create a Blueprint for the '/flask' prefix
flask_blueprint = Blueprint('flaskapi', __name__, url_prefix='/flaskapi')

# Initialize the API with the Blueprint
api = Api(
    flask_blueprint,
    version='1.0',
    title='Student API',
    description='API for student data',
    doc='/docs',  # Serve Swagger UI under /flask/docs
    static_url_path='/swaggerui',  # Serve Swagger assets
)

app.register_blueprint(flask_blueprint)

# Define API Endpoints
@api.route('/students')
class StudentList(Resource):
    def get(self):
        result = db.engine.execute("SELECT * FROM Students")
        students = [dict(row) for row in result]
        return students

if __name__ == '__main__':
    app.run(debug=True)
