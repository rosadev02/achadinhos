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

# Lê produtos do CSV (limita a 30)
df = pd.read_csv("data/ofertas_shopee.csv").head(30)

print(f"📸 Iniciando postagem de {len(df)} produtos no Instagram (feed + stories)...")

for i, produto in df.iterrows():
    legenda = gerar_legenda(produto)

    # ===== FEED =====
    container_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/media"
    payload_feed = {
        "image_url": produto["imageUrl"],
        "caption": legenda,
        "access_token": ACCESS_TOKEN
    }

    res_feed = requests.post(container_url, data=payload_feed)
    data_feed = res_feed.json()

    if "id" not in data_feed:
        print(f"❌ [{i+1}] Erro ao criar container do feed:", data_feed)
        continue

    creation_id_feed = data_feed["id"]
    time.sleep(3)

    publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/media_publish"
    res_publish_feed = requests.post(publish_url, data={
        "creation_id": creation_id_feed,
        "access_token": ACCESS_TOKEN
    })
    result_feed = res_publish_feed.json()

    if "id" in result_feed:
        print(f"✅ [{i+1}/30] Feed publicado com ID: {result_feed['id']}")
    else:
        print(f"❌ [{i+1}/30] Erro no feed:", result_feed)

    # ===== STORIES =====
    payload_story = {
        "image_url": produto["imageUrl"],
        "is_stories": "true",
        "media_type": "IMAGE",  # Essencial para não cair no Feed!
        "access_token": ACCESS_TOKEN
    }

    res_story = requests.post(container_url, data=payload_story)
    data_story = res_story.json()

    if "id" not in data_story:
        print(f"⚠️ [{i+1}/30] Erro ao criar container do story:", data_story)
        continue

    creation_id_story = data_story["id"]
    time.sleep(3)

    res_publish_story = requests.post(publish_url, data={
        "creation_id": creation_id_story,
        "access_token": ACCESS_TOKEN
    })
    result_story = res_publish_story.json()

    if "id" in result_story:
        print(f"✅ [{i+1}/30] Story publicado com ID: {result_story['id']}")
    else:
        print(f"⚠️ [{i+1}/30] Erro ao publicar story:", result_story)

    time.sleep(5)

print("🏁 Publicação concluída com sucesso!")
