from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    # Fetch the environment variable "SENV" and default to "NOT FOUND" if it does not exist
    environ = os.getenv("ENV", "NOT FOUND")
    return f'Hello from the first route! Environment variable SENV: {environ}'

@app.route('/hello')
def hello_hello():
    return 'Hello from the second route!'

if __name__ == '__main__':
    app.run(debug=True)
