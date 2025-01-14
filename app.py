from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def get_cookies():
    # Access cookies from the request
    username = request.cookies.get('username')
    email = request.cookies.get('email')
    authorize = request.cookies.get('authorize')
    
    return f'Username: {username}, Email: {email}, Authorize: {authorize}'

if __name__ == '__main__':
    app.run(debug=True)
