import os
import time
import requests
from dotenv import load_dotenv
from utils.sign import gerar_sign

load_dotenv()

PARTNER_ID = os.getenv("PARTNER_ID")
PARTNER_KEY = os.getenv("PARTNER_KEY")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_CODE = os.getenv("AUTH_CODE")

def obter_access_token():
    path = "/api/v2/auth/token/get"
    timestamp = int(time.time())
    sign = gerar_sign(PARTNER_ID, path, timestamp, PARTNER_KEY)

    url = f"https://partner.shopeemobile.com{path}"
    payload = {
        "code": AUTH_CODE,
        "partner_id": PARTNER_ID,
        "sign": sign,
        "timestamp": timestamp,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Access token obtido com sucesso!")
        print(response.json())
        return response.json()
    else:
        print("❌ Erro ao obter access token")
        print(response.status_code, response.text)
        return None
