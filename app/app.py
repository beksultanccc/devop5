from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "CI/CD жұмыс істейді!",
        "hits": 1
    })

@app.route("/add-user")
def add_user():
    return jsonify({
        "message": "Пайдаланушы қосылды"
    })

@app.route("/users")
def users():
    return jsonify({
        "users": ["JenkinsUser1", "JenkinsUser2", "JenkinsUser3"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
