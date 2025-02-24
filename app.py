from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

DJANGO_API_URL = "https://prod-quant.vaneck.com/user_data/"

# Create a session object to persist cookies
session = requests.Session()

@app.route("/get_user_data", methods=["GET"])
def get_user_data():
    # Automatically forward all cookies from the Flask request to the Django API
    response = session.get(DJANGO_API_URL, cookies=request.cookies)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
