
from flask import Flask, request, jsonify
from chatbot import Chatbot
import pathlib

app = Flask(__name__)
bot = Chatbot(str(pathlib.Path(__file__).parent / "patterns.json"))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    msg = data.get("message", "")
    return jsonify({"reply": bot.respond(msg)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
