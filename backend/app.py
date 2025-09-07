# backend/app.py
import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from transformers import pipeline
from functools import lru_cache

# device = -1 for CPU, set to 0 if using GPU on a server (not typical on Render)
DEVICE = -1

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)  # OK to keep for local dev / external frontends

# cached model loaders
@lru_cache(maxsize=4)
def get_summarizer(model_name="sshleifer/distilbart-cnn-12-6"):
    return pipeline("summarization", model=model_name, device=DEVICE)

@lru_cache(maxsize=2)
def get_qa(model_name="distilbert-base-cased-distilled-squad"):
    return pipeline("question-answering", model=model_name, device=DEVICE)

# Serve frontend
@app.route("/")
def home():
    return render_template("UI-study-assisstant.html")

# Healthcheck (useful)
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# API: Summarize
@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json(force=True)
    text = data.get("text", "")
    if not text or len(text.strip()) < 20:
        return jsonify({"error": "Please provide longer text"}), 400

    try:
        summarizer = get_summarizer()
        # make outputs shorter on deployed servers
        out = summarizer(text, max_length=500, min_length=150, do_sample=False)
        return jsonify({"summary": out[0]["summary_text"]})
    except Exception as e:
        return jsonify({"error": "Summarization failed: " + str(e)}), 500

# API: Q&A
@app.route("/api/qa", methods=["POST"])
def qa():
    data = request.get_json(force=True)
    text = data.get("text", "")
    question = data.get("question", "")
    if not text or not question:
        return jsonify({"error": "Please provide both text and question"}), 400
    try:
        qa_pipeline = get_qa()
        out = qa_pipeline(question=question, context=text)
        return jsonify(out)
    except Exception as e:
        return jsonify({"error": "Q&A failed: " + str(e)}), 500


# Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # host=0.0.0.0 so Render can reach it
    app.run(host="0.0.0.0", port=port, debug=True)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

