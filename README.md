# Investment ML — Local Demo

This small FastAPI app predicts investment objective and expected return.

Run locally:

```bash
pip install -r requirements.txt  # if you have requirements, e.g., fastapi, uvicorn, joblib, numpy
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Form guidance (encodings shown in the form):

- `liquidity_preference`: 0 = Low (long-term), 1 = Medium, 2 = High (need cash)
- `age_bucket_encoded`: 0 = <25, 1 = 25–34, 2 = 35–44, 3 = 45–54, 4 = 55+
- `investment_experience`: 0 = Beginner, 1 = Experienced
- `risk_score`: integer 1–10 (1 conservative, 10 aggressive)
- `investment_to_income_ratio`: percentage (0-100)

If you want, I can also:
- Add example data pre-filled in the form
- Replace selects with tooltips or inline examples
- Add automated tests or CI
