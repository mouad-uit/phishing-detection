# Phishing Detection Web App (XGBoost + Flask)

Simple school project that detects whether a website is **legitimate (0)** or
**phishing (1)** using a trained **XGBoost** model on URL and HTML features.

## 1. Prérequis

- Python 3.9+ recommandé

```bash
python -m venv .venv
source .venv/bin/activate  # sous Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Assurez-vous d'avoir exécuté le notebook `docs/XG-boost-model.ipynb` jusqu'à la
cellule d'export, pour générer:

- `model/phishing_xgb.pkl`
- `model/feature_order.json`

## 2. Lancer l'application en local

```bash
python app.py
```

Puis ouvrir dans le navigateur:

- http://localhost:5000

Entrez une URL, le modèle renvoie:

- `0` → site **légitime**
- `1` → site **phishing**

La page affiche aussi la probabilité estimée que le site soit du phishing.

## 3. Déploiement simple (ex: Render / Railway)

1. Pousser ce repo sur GitHub.
2. Créer un nouveau service web (Render, Railway, etc.).
3. Indiquer:
   - Commande de démarrage: `gunicorn app:app`
   - Fichier de dépendances: `requirements.txt`
4. Lancer le déploiement, puis ouvrir l'URL publique fournie.

## 4. Rappel pour le mini-rapport

- Entrée du modèle: ensemble de features extraites à partir:
  - de l'URL (longueur, nombre de chiffres, HTTPS, sous-domaines, etc.),
  - du HTML (présence de formulaire, mot de passe, iframes, images, etc.),
  - de quelques indicateurs simples de similarité entre titre et domaine/URL.
- Sortie du modèle:
  - `0 = site légitime`
  - `1 = site phishing`


