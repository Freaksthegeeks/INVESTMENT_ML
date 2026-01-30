# Investment ML — Local Demo ✅

A small FastAPI demo that predicts an investor's **investment objective** (classification) and an **expected annual return** (regression), then shows a 10-year projection for the invested amount.

---

## 🚀 Quick start

1. Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

2. Make sure the trained model files exist in the repo root:

- `classification_model.pkl` — classification model (investment objective)
- `regression_model.pkl` — regression model (expected annual return)

3. Run locally:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser at: http://127.0.0.1:8000

---

## 🔧 Features

- Web form UI (served at `/`) to enter investor inputs
- POST `/predict` accepts form fields and returns an HTML page with:
  - Predicted objective (Income / Capital Appreciation / Growth)
  - Estimated annual return (percent)
  - 10-year compounded projection chart

---

## 📡 Example — programmatic request

You can POST form data programmatically (the app expects standard form fields):

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -F "income=50000" \
  -F "investment_amount=10000" \
  -F "investment_to_income_ratio=20" \
  -F "risk_score=6" \
  -F "liquidity_preference=1" \
  -F "investment_experience=1" \
  -F "age_bucket_encoded=2"
```

The response is HTML (the same form page with results filled in).

---

## 📋 Form guidance (encodings shown in the UI)

- `liquidity_preference`: 0 = **Low (long-term)**, 1 = **Medium**, 2 = **High (need cash)**
- `age_bucket_encoded`: 0 = **<25**, 1 = **25–34**, 2 = **35–44**, 3 = **45–54**, 4 = **55+**
- `investment_experience`: 0 = **Beginner**, 1 = **Experienced**
- `risk_score`: integer **1–10** (1 conservative, 10 aggressive)
- `investment_to_income_ratio`: percentage **0–100**

---

## 🏗️ Architecture (Mermaid flow diagram)

```mermaid
flowchart LR
  U[User] -->|visit| F[Frontend: index.html]
  F -->|form submit| S[FastAPI Server]
  S --> P[Preprocessor]
  P --> CM[Classification model (classification_model.pkl)]
  P --> RM[Regression model (regression_model.pkl)]
  CM --> R1[Objective prediction]
  RM --> R2[Estimated annual return]
  R2 --> G[Compute 10-year projection]
  R1 & G --> V[Render results in templates/index.html]
  S -->|static files| ST[static/]
```

> Note: GitHub supports rendering Mermaid diagrams. If your viewer doesn't render them, try the VS Code "Markdown Preview Mermaid Support" extension or paste the diagram into https://mermaid.live/

---

## 💡 Tips & next steps

- Add example data pre-filled in the form (`templates/index.html`) for demonstration
- Add unit tests for model prediction code and a CI workflow
- Add an API-only JSON endpoint if you want programmatic JSON responses instead of HTML

---

## Contributing

Contributions welcome — fork, add tests, and open a PR.

---

## License

MIT
