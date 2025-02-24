from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

DJANGO_API_URL = "https://prod-quant.vaneck.com/user_data/"

@app.route("/get_user_data", methods=["GET"])
def get_user_data():
    response = requests.get(DJANGO_API_URL, cookies=request.cookies)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
