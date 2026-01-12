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


