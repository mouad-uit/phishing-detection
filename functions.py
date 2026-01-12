import re
import json
import joblib
import numpy as np
import pandas as pd
import requests

from difflib import SequenceMatcher
from urllib.parse import urlparse
from functools import lru_cache

from constants import KNOWN_LEGITIMATE_URLS


KNOWN_LEGITIMATE_URLS = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.amazon.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    # Ajoutez d'autres domaines légitimes selon votre besoin
]


FEATURE_ORDER = [
    "URLLength",
    "IsDomainIP",
    "URLSimilarityIndex",
    "CharContinuationRate",
    "TLDLegitimateProb",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "LetterRatioInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "SpacialCharRatioInURL",
    "LargestLineLength",
    "HasTitle",
    "URLTitleMatchScore",
    "HasFavicon",
    "Robots",
    "IsResponsive",
    "NoOfURLRedirect",
    "NoOfSelfRedirect",
    "HasDescription",
    "NoOfPopup",
    "NoOfiFrame",
    "HasExternalFormSubmit",
    "HasSocialNet",
    "HasSubmitButton",
    "HasHiddenFields",
    "HasPasswordField",
    "Bank",
    "Pay",
    "Crypto",
    "HasCopyrightInfo",
    "NoOfEmptyRef",
    "JS_to_CSS_ratio",
    "External_to_Self_ratio",
    "Code_density"
]


# =========================
# 1. VALIDATION & NORMALISATION
# =========================

def validateAndNormalizeData(request):
    data = request.get_json(silent=True)

    if data and "url" in data:
        url = data["url"].strip()
    else:
        url = request.form.get("url", "").strip()

    if not url:
        raise ValueError("Veuillez saisir une URL.")

    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("URL invalide.")

    return url


# =========================
# 2. FEATURE EXTRACTION
# =========================


def _url_similarity_index(url):
    """
    Compare l'URL avec la liste des URLs légitimes connues.
    Renvoie la valeur de similarité maximale entre 0 et 1.
    """
    url_domain = urlparse(url).netloc.lower()
    max_similarity = 0.0

    for legit_url in KNOWN_LEGITIMATE_URLS:
        legit_domain = urlparse(legit_url).netloc.lower()
        similarity = SequenceMatcher(None, url_domain, legit_domain).ratio()
        if similarity > max_similarity:
            max_similarity = similarity

    return max_similarity


def get_url_data(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    features = {}

    # ---- URL based features ----
    features["URLLength"] = len(url)
    features["DomainLength"] = len(domain)
    features["IsDomainIP"] = int(bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain)))
    features["TLDLength"] = len(domain.split(".")[-1])
    features["NoOfSubDomain"] = max(0, domain.count(".") - 1)

    features["NoOfEqualsInURL"] = url.count("=")
    features["NoOfQMarkInURL"] = url.count("?")
    features["NoOfAmpersandInURL"] = url.count("&")

    letters = sum(c.isalpha() for c in url)
    digits = sum(c.isdigit() for c in url)
    specials = len(url) - letters - digits

    features["LetterRatioInURL"] = letters / len(url)
    features["DegitRatioInURL"] = digits / len(url)
    features["SpacialCharRatioInURL"] = specials / len(url)

    features["HasObfuscation"] = int("%" in url or "@" in url)
    features["CharContinuationRate"] = _char_continuation_rate(url)

    features["URLSimilarityIndex"] = _url_similarity_index(url)

    # ---- Placeholder HTML features (to be improved later) ----
    html = _safe_fetch_html(url)

    features.update(_html_features(html, domain))

    return features


def _char_continuation_rate(text):
    max_repeat = 1
    current = 1
    for i in range(1, len(text)):
        if text[i] == text[i-1]:
            current += 1
            max_repeat = max(max_repeat, current)
        else:
            current = 1
    return max_repeat / len(text)


def _safe_fetch_html(url):
    try:
        r = requests.get(url, timeout=5)
        return r.text.lower()
    except Exception:
        return ""


def _html_features(html, domain):
    features = {}

    features["HasTitle"] = int("<title>" in html)
    features["HasFavicon"] = int("favicon" in html)
    features["HasDescription"] = int("meta name=\"description\"" in html)
    features["HasPasswordField"] = int("type=\"password\"" in html)
    features["HasSubmitButton"] = int("type=\"submit\"" in html)

    features["NoOfiFrame"] = html.count("<iframe")
    features["NoOfPopup"] = html.count("window.open")

    features["Bank"] = int(any(k in html for k in ["bank", "credit", "account"]))
    features["Pay"] = int(any(k in html for k in ["pay", "payment", "visa", "mastercard"]))
    features["Crypto"] = int(any(k in html for k in ["crypto", "bitcoin", "eth"]))

    features["LineOfCode"] = html.count("\n") + 1
    features["LargestLineLength"] = max((len(line) for line in html.split("\n")), default=0)

    return features


# =========================
# 3. MODEL CALL
# =========================

@lru_cache(maxsize=1)
def _load_model():
    return joblib.load("phishing_xgb.pkl")


@lru_cache(maxsize=1)
def _load_feature_order():
    with open("feature_order.json") as f:
        return json.load(f)


def sanitize_for_json(data):
    return {
        k: float(v) if hasattr(v, "item") else v
        for k, v in data.items()
    }



def callModel(features_dict):
    model = _load_model()

    X = np.array([[float(features_dict.get(f, 0)) for f in FEATURE_ORDER]])

    prediction = int(model.predict(X)[0])
    probability = float(model.predict_proba(X)[0][1])
    label = "Phishing" if prediction == 1 else "Legitimate",

    # probabilities = model.predict_proba(X)[:,1]
    # predictions = (probabilities >= 0.20).astype(int)
    # label = "Phishing" if predictions[0] == 0 else "Legitimate"
    # probability = probabilities[0]
    # prediction = predictions[0]

    print("\n--------------------------------------------------\n")
    print(f"Prediction: {prediction}, Label: {label}, Probability: {probability}")
    print("\n--------------------------------------------------\n")

    return {
        "prediction": prediction,  
        "label": label,
        "probability": round(probability, 4)
    }
