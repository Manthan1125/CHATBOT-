from flask import Flask, render_template, request
import json
from difflib import SequenceMatcher
import string

app = Flask(__name__)

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.strip()
    return text

def match_faq(user_msg, faq_data):
    user_msg_clean = clean_text(user_msg)
    best_match = None
    best_score = 0
    for item in faq_data:
        question_clean = clean_text(item["question"])
        score = SequenceMatcher(None, user_msg_clean, question_clean).ratio()
        if score > best_score:
            best_score = score
            best_match = item
    return best_match if best_score > 0.6 else None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_response():
    # Har request pe faq.json fresh load karo
    with open('data/faq.json') as f:
        faq_data = json.load(f)

    user_msg = request.form["msg"]
    matched = match_faq(user_msg, faq_data)
    if matched:
        return matched["answer"]
    else:
        return "Sorry, I don't have an answer for that right now. Please contact support."

if __name__ == "__main__":
    app.run(debug=True)
