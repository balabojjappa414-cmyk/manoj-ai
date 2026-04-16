from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]

    messages = [
        {"role": "system", "content": "Your name is MANOJ AI. You are a smart and helpful assistant created by Manoj."},
        {"role": "user", "content": user_message}
    ]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": messages
        }
    )

    data = response.json()

    if "choices" in data:
        return jsonify(data["choices"][0]["message"])
    else:
        return jsonify({"content": "Error: " + str(data)})

# ✅ IMPORTANT FIX FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port
   