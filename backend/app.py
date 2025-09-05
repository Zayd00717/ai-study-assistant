# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from functools import lru_cache

DEVICE = -1

app = Flask(__name__)
CORS(app)

@lru_cache(maxsize=4)
def get_summarizer(model_name="sshleifer/distilbart-cnn-12-6"):
    return pipeline("summarization", model=model_name, device=DEVICE)

@lru_cache(maxsize=2)
def get_qa(model_name="distilbert-base-cased-distilled-squad"):
    return pipeline("question-answering", model=model_name, device=DEVICE)

@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json() or {}
    text = data.get("text", "")
    if not text or len(text) < 50:
        return jsonify({"error": "Please provide longer text"}), 400
    summarizer = get_summarizer()
    result = summarizer(text, max_length=500, min_length=130, do_sample=False)
    return jsonify({"summary": result[0]["summary_text"]})

@app.route("/api/qa", methods=["POST"])
def qa():
    data = request.get_json() or {}
    text = data.get("text", "")
    question = data.get("question", "")
    if not text or not question:
        return jsonify({"error": "Please provide both text and question"}), 400
    qa_pipeline = get_qa()
    result = qa_pipeline(question=question, context=text)
    return jsonify(result)

@app.route("/")
def home():
    return "Hello from Flask on Render"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
