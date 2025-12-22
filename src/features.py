import math
import re
from typing import Dict, List, Optional

from urllib.parse import urlparse

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


def _safe_get_domain_parts(url: str) -> Dict[str, Optional[str]]:
    """
    Extract basic domain information from a URL without extra dependencies.
    Returns domain, tld, and full netloc.
    """
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    netloc = parsed.netloc or ""

    # Strip port if present
    if ":" in netloc:
        netloc = netloc.split(":", 1)[0]

    parts = netloc.split(".") if netloc else []

    if len(parts) >= 2:
        tld = parts[-1]
        domain = parts[-2]
    else:
        tld = None
        domain = netloc or None

    return {
        "netloc": netloc,
        "domain": domain,
        "tld": tld,
    }


def _is_ip_address(host: str) -> int:
    if not host:
        return 0
    # Very simple IPv4 check
    parts = host.split(".")
    if len(parts) != 4:
        return 0
    try:
        return 1 if all(0 <= int(p) <= 255 for p in parts) else 0
    except ValueError:
        return 0


def _count_characters(url: str) -> Dict[str, int]:
    return {
        "NoOfLettersInURL": sum(c.isalpha() for c in url),
        "NoOfDegitsInURL": sum(c.isdigit() for c in url),
        "NoOfEqualsInURL": url.count("="),
        "NoOfQMarkInURL": url.count("?"),
        "NoOfAmpersandInURL": url.count("&"),
    }


def _count_special_chars(url: str) -> Dict[str, int]:
    specials = "@$%^*()[]{}|\\;:'\",<>~`"
    count_other = sum(c in specials for c in url)
    return {
        "NoOfOtherSpecialCharsInURL": count_other,
    }


def _compute_obfuscation(url: str) -> Dict[str, float]:
    # Very simple approximation of obfuscation: repeated chars or encoded pieces
    repeated_pattern = re.compile(r"(.)\1\1+")  # aaa, ///, etc.
    matches = repeated_pattern.findall(url)
    no_of_obfuscated = len(matches)
    has_obfuscation = 1 if no_of_obfuscated > 0 else 0

    length = len(url) or 1
    obfuscation_ratio = no_of_obfuscated / length

    # CharContinuationRate is approximated by same indicator
    char_cont_rate = obfuscation_ratio

    return {
        "HasObfuscation": has_obfuscation,
        "NoOfObfuscatedChar": no_of_obfuscated,
        "ObfuscationRatio": obfuscation_ratio,
        "CharContinuationRate": char_cont_rate,
    }


def _fetch_html(url: str) -> Optional[str]:
    try:
        if not url.lower().startswith(("http://", "https://")):
            url = "http://" + url
        resp = requests.get(url, timeout=5)
        if resp.status_code >= 400:
            return None
        return resp.text
    except Exception:
        return None


def _extract_html_features(html: Optional[str]) -> Dict[str, float]:
    if not html:
        return {
            "LineOfCode": 0,
            "LargestLineLength": 0,
            "HasTitle": 0,
            "HasFavicon": 0,
            "Robots": 0,
            "IsResponsive": 0,
            "NoOfURLRedirect": 0,
            "NoOfSelfRedirect": 0,
            "HasDescription": 0,
            "NoOfPopup": 0,
            "NoOfiFrame": 0,
            "HasExternalFormSubmit": 0,
            "HasSocialNet": 0,
            "HasSubmitButton": 0,
            "HasHiddenFields": 0,
            "HasPasswordField": 0,
            "Bank": 0,
            "Pay": 0,
            "Crypto": 0,
            "HasCopyrightInfo": 0,
            "NoOfImage": 0,
            "NoOfCSS": 0,
            "NoOfJS": 0,
            "NoOfSelfRef": 0,
            "NoOfEmptyRef": 0,
            "NoOfExternalRef": 0,
            "DomainTitleMatchScore": 0.0,
            "URLTitleMatchScore": 0.0,
            "Title": "",
        }

    lines = html.splitlines()
    line_of_code = len(lines)
    largest_line_len = max((len(l) for l in lines), default=0)

    soup = BeautifulSoup(html, "html.parser")

    # Title and meta
    title_tag = soup.title
    title_text = title_tag.get_text(strip=True) if title_tag else ""
    has_title = 1 if title_text else 0

    has_description = 1 if soup.find("meta", attrs={"name": "description"}) else 0

    # Very rough heuristics for favicon and responsiveness
    has_favicon = 1 if soup.find("link", rel=lambda v: v and "icon" in v.lower()) else 0
    is_responsive = 1 if soup.find("meta", attrs={"name": "viewport"}) else 0

    # Elements counts
    no_img = len(soup.find_all("img"))
    no_css = len(soup.find_all("link", rel=lambda v: v and "stylesheet" in v.lower()))
    no_js = len(soup.find_all("script"))
    no_iframe = len(soup.find_all("iframe"))

    # Links statistics
    anchors = soup.find_all("a", href=True)
    no_empty_ref = sum(1 for a in anchors if a["href"] in ("", "#"))
    # Self vs external refs are filled later when we know the domain

    # Forms and security-related flags
    forms = soup.find_all("form")
    has_submit_button = 1 if soup.find("button", {"type": "submit"}) or soup.find(
        "input", {"type": "submit"}
    ) else 0
    has_hidden_fields = 1 if soup.find("input", {"type": "hidden"}) else 0
    has_password_field = 1 if soup.find("input", {"type": "password"}) else 0

    has_popup = 1 if "window.open(" in html or "alert(" in html else 0

    # Very rough keyword search in page text
    text = soup.get_text(separator=" ", strip=True).lower()
    bank = 1 if any(k in text for k in ["bank", "banque"]) else 0
    pay = 1 if any(k in text for k in ["pay", "paiement", "payment"]) else 0
    crypto = 1 if any(k in text for k in ["crypto", "bitcoin", "ethereum"]) else 0

    has_copyright = 1 if "copyright" in text or "©" in text else 0

    # Social networks
    has_social = 1 if any(
        s in html.lower()
        for s in ["facebook.com", "twitter.com", "instagram.com", "linkedin.com"]
    ) else 0

    # External form submit is approximated below in combination with URL

    return {
        "LineOfCode": line_of_code,
        "LargestLineLength": largest_line_len,
        "HasTitle": has_title,
        "Title": title_text,
        "HasFavicon": has_favicon,
        "Robots": 0,  # would require extra HTTP call; keep 0 for simplicity
        "IsResponsive": is_responsive,
        "NoOfURLRedirect": 0,  # not tracked in this simple version
        "NoOfSelfRedirect": 0,
        "HasDescription": has_description,
        "NoOfPopup": has_popup,
        "NoOfiFrame": no_iframe,
        "HasExternalFormSubmit": 0,  # filled later with domain if needed
        "HasSocialNet": has_social,
        "HasSubmitButton": has_submit_button,
        "HasHiddenFields": has_hidden_fields,
        "HasPasswordField": has_password_field,
        "Bank": bank,
        "Pay": pay,
        "Crypto": crypto,
        "HasCopyrightInfo": has_copyright,
        "NoOfImage": no_img,
        "NoOfCSS": no_css,
        "NoOfJS": no_js,
        "NoOfSelfRef": 0,  # filled later
        "NoOfEmptyRef": no_empty_ref,
        "NoOfExternalRef": 0,  # filled later
        "DomainTitleMatchScore": 0.0,
        "URLTitleMatchScore": 0.0,
    }


def build_feature_row(url: str, feature_order: List[str]) -> pd.DataFrame:
    """
    Build a single-row DataFrame with all features expected by the model.
    For any feature we don't explicitly compute, we default to 0.
    """
    original_url = url
    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    domain_info = _safe_get_domain_parts(url)

    url_length = len(url)
    domain = domain_info["domain"] or ""
    netloc = domain_info["netloc"] or ""
    tld = domain_info["tld"] or ""

    # Basic URL-related features
    # IMPORTANT: Apply log transform to match training data distribution
    # Training data shows URLLength as log values (e.g., 1.496434)
    url_length_log = np.log1p(url_length)  # log(1 + x) to handle 0
    
    # Encode TLD as numeric (deterministic: sum of character codes)
    # This converts TLD string to a consistent numeric value
    tld_encoded = float(sum(ord(c) for c in tld.lower()) if tld else 0)
    
    url_feats: Dict[str, float] = {
        "URLLength": url_length_log,  # Log transformed to match training
        "DomainLength": len(domain),
        "IsDomainIP": _is_ip_address(netloc),
        "TLDLength": len(tld),
        "NoOfSubDomain": max(0, netloc.count(".") - 1),
        "IsHTTPS": 1 if parsed.scheme == "https" else 0,
        "TLD": tld_encoded,  # Encoded as numeric for XGBoost compatibility
    }

    # Character counts and ratios
    counts = _count_characters(url)
    specials = _count_special_chars(url)
    obfusc = _compute_obfuscation(url)

    no_letters = counts["NoOfLettersInURL"]
    no_digits = counts["NoOfDegitsInURL"]
    no_other_special = specials["NoOfOtherSpecialCharsInURL"]
    
    # Apply log transform to NoOfLettersInURL to match training data
    # Training data shows NoOfLettersInURL as log values (e.g., 1.372307)
    counts["NoOfLettersInURL"] = np.log1p(no_letters)  # Update in counts dict

    letter_ratio = no_letters / url_length if url_length else 0.0
    digit_ratio = no_digits / url_length if url_length else 0.0
    special_ratio = no_other_special / url_length if url_length else 0.0

    ratio_feats = {
        "LetterRatioInURL": letter_ratio,
        "DegitRatioInURL": digit_ratio,
        "SpacialCharRatioInURL": special_ratio,
    }

    # HTML-based features
    html = _fetch_html(original_url)
    html_feats = _extract_html_features(html)

    # Approximate URL/domain vs title similarity with simple overlap
    # IMPORTANT: Training data shows scores as percentages (0-100), not ratios (0-1)
    if html_feats["Title"]:
        title_lower = html_feats["Title"].lower()
        # Domain-title similarity (as percentage like in training data)
        common_chars = set(domain.lower()) & set(title_lower)
        denom = len(set(domain.lower())) or 1
        domain_title_score = (len(common_chars) / denom) * 100.0  # Scale to 0-100
        # URL-title similarity (as percentage)
        common_chars_url = set(original_url.lower()) & set(title_lower)
        denom_url = len(set(original_url.lower())) or 1
        url_title_score = (len(common_chars_url) / denom_url) * 100.0  # Scale to 0-100
    else:
        domain_title_score = 0.0
        url_title_score = 0.0

    html_feats["DomainTitleMatchScore"] = domain_title_score
    html_feats["URLTitleMatchScore"] = url_title_score

    # Default / placeholder values for complex statistical features
    # IMPORTANT: Training data shows URLSimilarityIndex around 100.0, not 0.5!
    # Use more realistic defaults based on training data distribution
    complex_defaults = {
        "URLSimilarityIndex": 100.0,  # Most URLs in training have 100.0
        "TLDLegitimateProb": 0.5,  # This seems correct based on training data
        "URLCharProb": 0.05,  # Training data shows values around 0.05-0.06
    }

    # Merge all partial dictionaries into one flat feature dict
    all_feats: Dict[str, float] = {}
    all_feats.update(url_feats)
    all_feats.update(counts)
    all_feats.update(specials)
    all_feats.update(obfusc)
    all_feats.update(ratio_feats)
    all_feats.update(html_feats)
    all_feats.update(complex_defaults)

    # Now create a row with all expected features
    row = {col: 0 for col in feature_order}
    for key, value in all_feats.items():
        if key in row:
            row[key] = value

    df = pd.DataFrame([row], columns=feature_order)
    return df


