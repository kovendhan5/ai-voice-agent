"""
Super Simple Test Server
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def test():
    return jsonify({"status": "working", "message": "Server is alive!"})

if __name__ == '__main__':
    print("Starting test server on port 8080...")
    app.run(host='0.0.0.0', port=8080)
