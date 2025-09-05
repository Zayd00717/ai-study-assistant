const API = "http://localhost:5000/api";

document.getElementById("summarize").onclick = async () => {
  const text = document.getElementById("text").value;
  const res = await fetch(`${API}/summarize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });
  const data = await res.json();
  document.getElementById("output").textContent = data.summary || data.error;
};

document.getElementById("ask").onclick = async () => {
  const text = document.getElementById("text").value;
  const question = document.getElementById("question").value;
  const res = await fetch(`${API}/qa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, question })
  });
  const data = await res.json();
  document.getElementById("output").textContent = data.answer 
    ? `Answer: ${data.answer} (confidence: ${Math.min(Math.max(data.score*100, 0), 100).toFixed(1)}%)`
    : data.error;
};

