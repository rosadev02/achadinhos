import pandas as pd
import requests
import os
import time
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")
ACCESS_TOKEN = os.getenv("PAGE_TOKEN")

# Gera legenda com chamada para link da bio
def gerar_legenda(prod):
    return f"""🛍️ {prod["productName"]}

💰 R$ {prod["price"]}
🏬 {prod["shopName"]}
⭐ {prod.get("ratingStar", "?")} estrelas

👉 Confira no link da bio!
#achadinhos #promo #shopee #ofertas"""

# Lê produtos do CSV
df = pd.read_csv("data/ofertas_shopee.csv")

print(f"📸 Iniciando postagem de {len(df)} produtos no Instagram...")

for i, produto in df.iterrows():
    legenda = gerar_legenda(produto)

    # Etapa 1: Cria o container de mídia
    container_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/media"
    payload_container = {
        "image_url": produto["imageUrl"],
        "caption": legenda,
        "access_token": ACCESS_TOKEN
    }

    res_container = requests.post(container_url, data=payload_container)
    data_container = res_container.json()

    if "id" not in data_container:
        print(f"❌ [{i+1}] Erro ao criar container:", data_container)
        continue

    creation_id = data_container["id"]
    time.sleep(3)  # Espera o container ser processado

    # Etapa 2: Publica o post
    publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/media_publish"
    payload_publish = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }

    res_publish = requests.post(publish_url, data=payload_publish)
    data_publish = res_publish.json()

    if "id" in data_publish:
        print(f"✅ [{i+1}/{len(df)}] Produto publicado com ID: {data_publish['id']}")
    else:
        print(f"❌ [{i+1}/{len(df)}] Erro ao publicar:", data_publish)

    time.sleep(5)  # Delay entre publicações

print("🏁 Finalizado!")
