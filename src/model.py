import json
from urllib.parse import urlparse
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
    proba = float(model.predict_proba(X)[0][1]) if hasattr(model, "predict_proba") else 0.0

    row = X.iloc[0].to_dict()

    parsed = urlparse(url)

    details = {
        # --- META INFO (non-ML) ---
        "FILENAME": os.path.basename(parsed.path),
        "URL": url,
        "Domain": parsed.netloc.split(":")[0],
        # --- URL FEATURES ---
        "URLLength": row["URLLength"],
        "DomainLength": row["DomainLength"],
        "IsDomainIP": bool(row["IsDomainIP"]),
        "TLD": row["TLD"],
        "TLDLength": row["TLDLength"],
        "NoOfSubDomain": row["NoOfSubDomain"],
        "IsHTTPS": bool(row["IsHTTPS"]),
        "URLSimilarityIndex": row["URLSimilarityIndex"],
        "CharContinuationRate": row["CharContinuationRate"],
        "TLDLegitimateProb": row["TLDLegitimateProb"],
        "URLCharProb": row["URLCharProb"],
        # --- OBFUSCATION & CHARACTERS ---
        "HasObfuscation": bool(row["HasObfuscation"]),
        "NoOfObfuscatedChar": row["NoOfObfuscatedChar"],
        "ObfuscationRatio": row["ObfuscationRatio"],
        "NoOfLettersInURL": row["NoOfLettersInURL"],
        "LetterRatioInURL": row["LetterRatioInURL"],
        "NoOfDegitsInURL": row["NoOfDegitsInURL"],
        "DegitRatioInURL": row["DegitRatioInURL"],
        "NoOfEqualsInURL": row["NoOfEqualsInURL"],
        "NoOfQMarkInURL": row["NoOfQMarkInURL"],
        "NoOfAmpersandInURL": row["NoOfAmpersandInURL"],
        "NoOfOtherSpecialCharsInURL": row["NoOfOtherSpecialCharsInURL"],
        "SpacialCharRatioInURL": row["SpacialCharRatioInURL"],
        # --- HTML & PAGE STRUCTURE ---
        "LineOfCode": row["LineOfCode"],
        "LargestLineLength": row["LargestLineLength"],
        "HasTitle": bool(row["HasTitle"]),
        "Title": row.get("Title", ""),
        "DomainTitleMatchScore": row["DomainTitleMatchScore"],
        "URLTitleMatchScore": row["URLTitleMatchScore"],
        "HasFavicon": bool(row["HasFavicon"]),
        "Robots": bool(row["Robots"]),
        "IsResponsive": bool(row["IsResponsive"]),
        "NoOfURLRedirect": row["NoOfURLRedirect"],
        "NoOfSelfRedirect": row["NoOfSelfRedirect"],
        "HasDescription": bool(row["HasDescription"]),
        "NoOfPopup": row["NoOfPopup"],
        "NoOfiFrame": row["NoOfiFrame"],
        # --- FORMS & SECURITY ---
        "HasExternalFormSubmit": bool(row["HasExternalFormSubmit"]),
        "HasSubmitButton": bool(row["HasSubmitButton"]),
        "HasHiddenFields": bool(row["HasHiddenFields"]),
        "HasPasswordField": bool(row["HasPasswordField"]),
        # --- CONTENT & LINKS ---
        "HasSocialNet": bool(row["HasSocialNet"]),
        "Bank": bool(row["Bank"]),
        "Pay": bool(row["Pay"]),
        "Crypto": bool(row["Crypto"]),
        "HasCopyrightInfo": bool(row["HasCopyrightInfo"]),
        "NoOfImage": row["NoOfImage"],
        "NoOfCSS": row["NoOfCSS"],
        "NoOfJS": row["NoOfJS"],
        "NoOfSelfRef": row["NoOfSelfRef"],
        "NoOfEmptyRef": row["NoOfEmptyRef"],
        "NoOfExternalRef": row["NoOfExternalRef"],
    }

    return {
        "prediction": pred,
        "label": "Phishing" if pred == 1 else "Legitimate",
        "probability": proba,
        "details": details,
    }


