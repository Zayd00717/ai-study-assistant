const API = "/api";

function showOutput(text) {
  document.getElementById("output").textContent = text;
}

async function postJson(path, payload) {
  try {
    const res = await fetch(API + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    return { ok: res.ok, data };
  } catch (err) {
    return { ok: false, error: err.message || "Network error" };
  }
}

document.getElementById("summarize").onclick = async () => {
  const text = document.getElementById("text").value;
  if (!text || text.trim().length < 10) {
    showOutput("Please paste at least a short paragraph to summarize.");
    return;
  }
  showOutput("Summarizing... please wait.");
  const result = await postJson("/summarize", { text });
  if (!result.ok) {
    showOutput("Error: " + (result.data?.error || result.error || "Unknown error"));
  } else {
    showOutput(result.data.summary || "No summary returned.");
  }
};

document.getElementById("ask").onclick = async () => {
  const text = document.getElementById("text").value;
  const question = document.getElementById("question").value;
  if (!text || !question) {
    showOutput("Please provide both notes and a question.");
    return;
  }
  showOutput("Answering... please wait.");
  const result = await postJson("/qa", { text, question });
  if (!result.ok) {
    showOutput("Error: " + (result.data?.error || result.error || "Unknown error"));
  } else {
    const d = result.data;
    showOutput(d.answer ? `Answer: ${d.answer} (confidence: ${(d.score*100).toFixed(1)}%)` : JSON.stringify(d));
  }
};
