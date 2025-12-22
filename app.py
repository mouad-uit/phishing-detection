import os

from flask import Flask, render_template, request

from src.model import predict_url


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", result=None, error=None, url_value="")


@app.route("/predict", methods=["POST"])
def predict():
    url = request.form.get("url", "").strip()
    if not url:
        return render_template(
            "index.html",
            result=None,
            error="Veuillez saisir une URL.",
            url_value=url,
        )

    try:
        result = predict_url(url)
        return render_template(
            "index.html",
            result=result,
            error=None,
            url_value=url,
        )
    except Exception as e:
        return render_template(
            "index.html",
            result=None,
            error=f"Erreur lors de la prédiction : {e}",
            url_value=url,
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # Default to 5001 to avoid macOS AirPlay conflict
    app.run(host="0.0.0.0", port=port, debug=True)


