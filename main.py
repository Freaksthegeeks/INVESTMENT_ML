from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import numpy as np
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load models
classification_model = joblib.load("classification_model.pkl")
regression_model = joblib.load("regression_model.pkl")

# Mapping classification output to labels
objective_labels = {
    0: "Income",
    1: "Capital Appreciation",
    2: "Growth"
}

@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
def predict(
    request: Request,
    income: float = Form(...),
    investment_amount: float = Form(...),
    investment_to_income_ratio: float = Form(...),
    risk_score: float = Form(...),
    liquidity_preference: float = Form(...),
    investment_experience: int = Form(...),
    age_bucket_encoded: int = Form(...)
):
    input_data = np.array([
        income,
        investment_amount,
        investment_to_income_ratio,
        risk_score,
        liquidity_preference,
        investment_experience,
        age_bucket_encoded
    ]).reshape(1, -1)

    # Predict
    objective_pred = classification_model.predict(input_data)[0]
    return_pct_pred = regression_model.predict(input_data)[0]
    # Create a 10-year projection for the invested amount using the predicted annual return
    years = list(range(0, 11))
    try:
        factor = 1 + float(return_pct_pred) / 100.0
    except Exception:
        factor = 1.0
    values = [(investment_amount * (factor ** y)) for y in years]
    chart_data = [{"year": int(y), "value": float(v)} for y, v in zip(years, values)]

    explanation = (
        f"Predicted objective: {objective_labels.get(objective_pred, 'Unknown')}. "
        f"Estimated annual return: {return_pct_pred:.2f}%. "
        "The chart shows projected growth of the invested amount over 10 years (compounded annually)."
    )

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result_objective": objective_labels.get(objective_pred, "Unknown"),
        "result_return": f"{return_pct_pred:.2f}%",
        "chart_data": json.dumps(chart_data),
        "result_explanation": explanation,
    })
