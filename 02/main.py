from flask import Flask
import requests


app = Flask(__name__)


@app.route("/")
def view_root():
    return {}


@app.route("/health")
def view_health():
    return {
        "status": "ok",
        "v": "2"
    }


@app.route("/exchange-rate")
def view_exchange_rate():
    data = requests.get("https://www.sunat.gob.pe/a/txt/tipoCambio.txt")
    raw_data = data.text
    raw = raw_data.split("|")
    return {
        "date": raw[0],
        "sell": float(raw[1]),
        "buy": float(raw[2])
    }