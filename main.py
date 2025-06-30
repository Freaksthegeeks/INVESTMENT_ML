from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import joblib
import numpy as np

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

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result_objective": objective_labels.get(objective_pred, "Unknown"),
        "result_return": f"{return_pct_pred:.2f}%",
    })
