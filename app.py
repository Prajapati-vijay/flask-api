from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  #

app = Flask(__name__)

# Replace with your SQL Server connection details
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://SA:vijay123@docker.host.local/student?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/students', methods=['GET'])
def get_students():
    # Use the text function to wrap the raw SQL query
    sql = text("SELECT * FROM students")
    result = db.session.execute(sql)
    
    # Get column names
    columns = result.keys()
    
    # Convert each row into a dictionary
    students = [dict(zip(columns, row)) for row in result]
    
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)
