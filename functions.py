import re
import json
import joblib
import numpy as np
import pandas as pd
import requests

from difflib import SequenceMatcher
from urllib.parse import urlparse
from functools import lru_cache

from constants import KNOWN_LEGITIMATE_URLS, LEGITIMATE_TLDS, FEATURE_ORDER



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


def _has_hidden_fields(html):
    try:
        return int(bool(re.search(r'<input[^>]+type=["\']hidden["\']', html, re.IGNORECASE)))
    except Exception:
        return 0


def _has_social_net(html):
    SOCIAL_DOMAINS = [
        "facebook.com", "twitter.com", "linkedin.com", "instagram.com",
        "pinterest.com", "tiktok.com", "snapchat.com", "reddit.com"
    ]
    try:
        return int(any(domain in html for domain in SOCIAL_DOMAINS))
    except Exception:
        return 0



def _has_external_form_submit(html, url):
    from urllib.parse import urlparse
    try:
        domain = urlparse(url).netloc.lower()
        matches = re.findall(r'<form[^>]+action=["\'](.*?)["\']', html, re.IGNORECASE)
        for action in matches:
            action_domain = urlparse(action).netloc.lower()
            if action_domain and action_domain != domain:
                return 1
        return 0
    except Exception:
        return 0


def _count_redirects(url):
    """
    Retourne (total_redirects, self_redirects)
    """
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        total_redirects = len(r.history)
        self_redirects = sum(1 for resp in r.history if resp.url.rstrip('/') == url.rstrip('/'))

        return total_redirects, self_redirects
    except Exception:
        return 0, 0



def _is_responsive(html):
    try:
        if '<meta name="viewport"' in html:
            return 1
        if '@media' in html:
            return 1
        return 0
    except Exception:
        return 0



def _has_robots_txt(url):
    from urllib.parse import urljoin
    try:
        robots_url = urljoin(url, "/robots.txt")
        r = requests.get(robots_url, timeout=5)
        return int(r.status_code == 200)
    except Exception:
        return 0


def _url_title_match_score(html, url):
    """
    Compare l'URL et le <title> de la page.
    Retourne une valeur de similarité entre 0 et 1.
    """
    from difflib import SequenceMatcher
    from urllib.parse import urlparse

    try:
        # Extraire le contenu de <title>
        match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if not match:
            return 0.0
        title = match.group(1).strip().lower()

        # Extraire le domaine de l'URL
        domain = urlparse(url).netloc.lower()

        # Similarité
        return SequenceMatcher(None, domain, title).ratio()
    except Exception:
        return 0.0


def _tld_legitimate_prob(url):
    """
    Retourne la probabilité que le TLD soit légitime, entre 0 et 1.
    Si TLD inconnu, retourne une valeur par défaut (0.5).
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    tld = domain.split(".")[-1] if "." in domain else ""
    return LEGITIMATE_TLDS.get(tld, 0.5)


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
    features["DigitRatioInURL"] = digits / len(url)
    features["SpacialCharRatioInURL"] = specials / len(url)

    features["HasObfuscation"] = int("%" in url or "@" in url)
    features["CharContinuationRate"] = _char_continuation_rate(url)

    features["URLSimilarityIndex"] = _url_similarity_index(url)
    features["TLDLegitimateProb"] = _tld_legitimate_prob(url)

    # ---- Placeholder HTML features (to be improved later) ----
    html = _safe_fetch_html(url)

    features.update(_html_features(html, domain, url))

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


def _html_advanced_features(html, domain):
    """
    Extract advanced HTML/JS/CSS features that were missing:
    - HasCopyrightInfo
    - NoOfEmptyRef
    - JS_to_CSS_ratio
    - External_to_Self_ratio
    - Code_density
    """
    from urllib.parse import urlparse

    features = {}

    # 1️⃣ HasCopyrightInfo
    features["HasCopyrightInfo"] = int(bool(re.search(r'©|copyright', html, re.IGNORECASE)))

    # 2️⃣ NoOfEmptyRef
    # Count <a href=""> or <a href="#"> links
    features["NoOfEmptyRef"] = len(re.findall(r'<a\s+[^>]*href=["\']\s*(#|)["\']', html, re.IGNORECASE))

    # 3️⃣ JS_to_CSS_ratio
    js_len = sum(len(m.group(0)) for m in re.finditer(r'<script[^>]*>.*?</script>', html, re.DOTALL))
    css_len = sum(len(m.group(0)) for m in re.finditer(r'<style[^>]*>.*?</style>', html, re.DOTALL))
    # Avoid division by zero
    features["JS_to_CSS_ratio"] = js_len / css_len if css_len > 0 else js_len

    # 4️⃣ External_to_Self_ratio
    # Count all <a href="..."> links and determine if they are external
    all_links = re.findall(r'<a\s+[^>]*href=["\'](.*?)["\']', html, re.IGNORECASE)
    external_links = 0
    self_links = 0
    for link in all_links:
        parsed_link = urlparse(link)
        if parsed_link.netloc and parsed_link.netloc.lower() != domain.lower():
            external_links += 1
        else:
            self_links += 1
    features["External_to_Self_ratio"] = (external_links / self_links) if self_links > 0 else external_links

    # 5️⃣ Code_density
    # Measure ratio of code (scripts/styles) vs total HTML length
    total_len = len(html)
    code_len = js_len + css_len
    features["Code_density"] = code_len / total_len if total_len > 0 else 0

    return features



def _html_features(html, domain, url):
    features = {}

    features["HasTitle"] = int("<title>" in html)
    features["URLTitleMatchScore"] = _url_title_match_score(html, url)
    features["HasFavicon"] = int("favicon" in html)
    features["Robots"] = _has_robots_txt(url)
    features["IsResponsive"] = _is_responsive(html)
    redirects, self_redirects = _count_redirects(url)
    features["NoOfURLRedirect"] = redirects
    features["NoOfSelfRedirect"] = self_redirects
    features["HasDescription"] = int('meta name="description"' in html)
    features["NoOfPopup"] = html.count("window.open")
    features["NoOfiFrame"] = html.count("<iframe")
    features["HasExternalFormSubmit"] = _has_external_form_submit(html, url)
    features["HasSocialNet"] = _has_social_net(html)
    features["HasSubmitButton"] = int('type="submit"' in html)
    features["HasHiddenFields"] = _has_hidden_fields(html)
    features["HasPasswordField"] = int('type="password"' in html)

    features["Bank"] = int(any(k in html for k in ["bank", "credit", "account"]))
    features["Pay"] = int(any(k in html for k in ["pay", "payment", "visa", "mastercard"]))
    features["Crypto"] = int(any(k in html for k in ["crypto", "bitcoin", "eth"]))

    features["LineOfCode"] = html.count("\n") + 1
    features["LargestLineLength"] = max((len(line) for line in html.split("\n")), default=0)

    features.update(_html_advanced_features(html, domain))

    return features



# =========================
# 3. MODEL CALL
# =========================

@lru_cache(maxsize=1)
def _load_model():
    return joblib.load("phishing_xgb.pkl")




def sanitize_for_json(data):
    return {
        k: float(v) if hasattr(v, "item") else v
        for k, v in data.items()
    }



def callModel(features_dict):
    model = _load_model()

    X = np.array([[float(features_dict.get(f, 0)) for f in FEATURE_ORDER]])

    # prediction = int(model.predict(X)[0])
    # probability = float(model.predict_proba(X)[0][1])
    # label = "Phishing" if prediction == 0 else "Legitimate"


    probabilities = model.predict_proba(X)[:,1]
    predictions = (probabilities >= 0.20).astype(int)
    label = "Phishing" if predictions[0] == 0 else "Legitimate"
    prediction = int(predictions[0])
    probability = float(probabilities[0])

    print("\n--------------------------------------------------")
    print(f"Prediction: {prediction}, Label: {label}, Probability: {probability}")
    print("\n--------------------------------------------------")

    return {
        "prediction": prediction,  
        "label": label,
        "probability": round(probability, 4)
    }
