from flask import Flask, jsonify, render_template_string
import requests

app = Flask(__name__)

@app.route('/')
def fetch_userauth_data():
    try:
        # Request data from the userauth endpoint
        response = requests.get("http://localhost:8082/userauth/")
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        data = response.json()
        return render_template_string("""
            <!DOCTYPE html>
            <html>
            <head><title>User Auth Data</title></head>
            <body>
                <h1>User Auth API Data</h1>
                <pre>{{ data }}</pre>
            </body>
            </html>
        """, data=data)
    except requests.exceptions.RequestException as e:
        # Handle errors in making the request
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
