import json
import os
from functools import lru_cache
from typing import Any, Dict

import joblib

from .features import build_feature_row


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "phishing_xgb.pkl")
FEATURE_ORDER_PATH = os.path.join(BASE_DIR, "model", "feature_order.json")


@lru_cache(maxsize=1)
def load_feature_order():
    with open(FEATURE_ORDER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def load_model():
    return joblib.load(MODEL_PATH)


def predict_url(url: str) -> Dict[str, Any]:
    """
    Build features for the given URL, run the XGBoost model,
    and return a small dictionary with prediction, label and probability.
    """
    feature_order = load_feature_order()
    model = load_model()

    X = build_feature_row(url, feature_order)

    pred = int(model.predict(X)[0])

    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(X)[0][1])
    else:
        proba = 0.0

    label_text = "Phishing" if pred == 1 else "Legitimate"

    return {
        "prediction": pred,
        "label": label_text,
        "probability": proba,
    }


