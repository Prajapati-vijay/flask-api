from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from the first route!'

@app.route('/hello')
def hello_hello():
    return 'Hello from the second route!'

if __name__ == '__main__':
    app.run(debug=True)
