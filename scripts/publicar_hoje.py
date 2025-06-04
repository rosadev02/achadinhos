import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
PAGE_ID = os.getenv("PAGE_ID")
ACCESS_TOKEN = os.getenv("PAGE_TOKEN")

# Função para gerar a legenda do post
def gerar_legenda(prod):
    return f"""🛒 {prod["productName"]}

💰 Por apenas R$ {prod["price"]}
⭐ Avaliação: {prod.get("ratingStar", "?")} estrelas
🏬 Loja: {prod["shopName"]}

🔗 Confira: {prod["offerLink"]}
#achadinhos #promo #shopee #ofertas"""

# URL da API do Facebook
GRAPH_URL = f"https://graph.facebook.com/{PAGE_ID}/photos"

# Lê o CSV de produtos
df = pd.read_csv("data/ofertas_shopee.csv")

print(f"📤 Iniciando postagem de {len(df)} produtos no Facebook...")

for i, produto in df.iterrows():
    legenda = gerar_legenda(produto)

    payload = {
        "url": produto["imageUrl"],
        "caption": legenda,
        "access_token": ACCESS_TOKEN
    }

    try:
        response = requests.post(GRAPH_URL, data=payload)

        if response.status_code == 200:
            post_id = response.json().get("post_id", response.json())
            print(f"✅ [{i+1}/{len(df)}] Produto postado com sucesso! ID: {post_id}")
        else:
            print(f"❌ [{i+1}/{len(df)}] Erro ao postar:")
            print("Status:", response.status_code)
            print("Resposta:", response.text)

        time.sleep(5)  # Aguarda 5 segundos entre as postagens
    except Exception as e:
        print(f"⚠️ [{i+1}] Erro inesperado:", e)

print("🏁 Finalizado!")
