import pandas as pd
import requests
import os
import time
import json
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# Carrega variáveis de ambiente
load_dotenv()
INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")
ACCESS_TOKEN = os.getenv("PAGE_TOKEN")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# Gera legenda para o feed
def gerar_legenda(prod):
    return f"""🛍️ {prod["productName"]}

💰 R$ {prod["price"]}
🏬 {prod["shopName"]}
⭐ {prod.get("ratingStar", "?")} estrelas

👉 Confira no link da bio!
#achadinhos #promo #shopee #ofertas"""

# Cria imagem vertical com fundo roxo e info do produto
def gerar_imagem_vertical(prod):
    largura, altura = 1080, 1920
    imagem = Image.new("RGB", (largura, altura), (128, 0, 128))  # Fundo roxo
    draw = ImageDraw.Draw(imagem)

    try:
        fonte_titulo = ImageFont.truetype("arialbd.ttf", 60)
        fonte_info = ImageFont.truetype("arial.ttf", 50)
    except:
        fonte_titulo = fonte_info = ImageFont.load_default()

    # Baixa imagem do produto
    response = requests.get(prod["imageUrl"])
    img_prod = Image.open(BytesIO(response.content)).resize((800, 800))

    # Coloca imagem centralizada
    imagem.paste(img_prod, (140, 250))

    # Texto superior
    draw.text((100, 1100), prod["productName"][:40], fill="white", font=fonte_titulo)
    draw.text((100, 1200), f'R$ {prod["price"]} - {prod["shopName"]}', fill="white", font=fonte_info)

    # Salva temporariamente
    caminho = f"tmp/story_{prod['productName'][:10]}.jpg"
    os.makedirs("tmp", exist_ok=True)
    imagem.save(caminho)
    return caminho

# Envia imagem para Imgbb e retorna link
def upload_para_imgbb(caminho):
    with open(caminho, "rb") as file:
        res = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": IMGBB_API_KEY},
            files={"image": file}
        )
    return res.json()["data"]["url"]

# Lê CSV e limita a 30 produtos
df = pd.read_csv("data/ofertas_shopee.csv").head(30)

print(f"📸 Iniciando postagem de {len(df)} produtos no Instagram (feed + stories)...")

for i, produto in df.iterrows():
    legenda = gerar_legenda(produto)
    image_url = produto["imageUrl"]
    link_afiliado = produto["offerLink"]

    # ========== FEED ==========
    feed_container_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/media"
    payload_feed = {
        "image_url": image_url,
        "caption": legenda,
        "access_token": ACCESS_TOKEN
    }

    res_feed = requests.post(feed_container_url, data=payload_feed)
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
        print(f"❌ [{i+1}/30] Erro ao publicar no feed:", result_feed)

    # ========== STORIES ==========
    caminho_img = gerar_imagem_vertical(produto)
    url_imgbb = upload_para_imgbb(caminho_img)

    payload_story = {
        "image_url": url_imgbb,
        "media_type": "STORIES",
        "access_token": ACCESS_TOKEN,
        "link_sticker": json.dumps([
            {
                "url": link_afiliado,
                "type": "standard",
                "position": {"x": 0.5, "y": 0.85},
                "size": {"width": 0.4, "height": 0.1}
            }
        ])
    }

    res_story = requests.post(feed_container_url, data=payload_story)
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
