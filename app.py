from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_restx import Api, Resource, fields
from flask import redirect
from flask_restx.apidoc import apidoc
import os
from werkzeug.middleware.proxy_fix import ProxyFix
# static_url_path = os.getenv('STATIC_URL_PATH', '/flask')
# apidoc.static_url_path = static_url_path

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_port=1, x_for=1, x_host=1, x_prefix=1)
# Replace with your SQL Server connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SA:vijay123@host.docker.internal/student?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['STATIC_URL_PATH'] = '/myapp/static'
db = SQLAlchemy(app)

# Create API object
api = Api(app, doc='/apidocs/')  # Swagger UI will be available at /apidocs

# Define the student model (Swagger model)
student_model = api.model('Student', {
    'id': fields.Integer(description='The student ID'),
    'name': fields.String(description='The student\'s name'),
    'age': fields.Integer(description='The student\'s age')
})

# Define the resource for `/students` endpoint
@api.route('/students')
class StudentList(Resource):
    @api.doc('get_all_students')
    @api.marshal_with(student_model, as_list=True)  # Marshals the response using student_model
    def get(self):
        """
        Get all students
        ---
        responses:
          200:
            description: A list of students
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Student'
        """
        sql = text("SELECT * FROM students")
        result = db.session.execute(sql)
        
        # Get column names
        columns = result.keys()
        
        # Convert each row into a dictionary
        students = [dict(zip(columns, row)) for row in result]
        
        return students

# @app.route('/')
# def index():
#     return redirect('/apidocs')  # Redirect to Swagger UI documentation

if __name__ == '__main__':
    app.run(debug=True)
