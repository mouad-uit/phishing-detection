import os
from urllib.parse import urlparse

from flask import Flask, render_template, request, jsonify

from functions import (
    validateAndNormalizeData,
    get_url_data,
    callModel,
    sanitize_for_json
)


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def validate_url(url: str):
    """
    Validate URL format.
    Returns (is_valid, error_message)
    """
    if not url or not url.strip():
        return False, "Veuillez saisir une URL."

    url = url.strip()

    # Add protocol if missing
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        parsed = urlparse(url)
        
        # Check if we have at least a netloc (domain)
        if not parsed.netloc:
            return False, "Format d'URL invalide. Veuillez entrer une URL valide (ex: https://www.example.com)"

        # Check if netloc looks like a domain or IP
        netloc = parsed.netloc.split(":")[0]  # Remove port if present
        
        # Basic domain/IP validation
        if not (netloc.count(".") >= 1 or netloc.replace(".", "").replace(":", "").isdigit()):
            return False, "Format d'URL invalide. Le domaine ou l'adresse IP est incorrect."

        return True, ""
    except Exception:
        return False, "Format d'URL invalide. Veuillez entrer une URL valide (ex: https://www.example.com)"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        url = validateAndNormalizeData(request)
        features = get_url_data(url)
        model_result = callModel(features)

        features = sanitize_for_json(features)

        return jsonify({
            "success": True,
            "url": url,
            "model": model_result,
            "features": features
        })

    except Exception as e:
        print("BACKEND ERROR >>>", repr(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Default to 5001 to avoid macOS AirPlay conflict
    app.run(host="0.0.0.0", port=port, debug=True)


