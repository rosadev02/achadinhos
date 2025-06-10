import os
import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
ACCESS_TOKEN = os.getenv("PAGE_TOKEN")
INSTAGRAM_ID = os.getenv("INSTAGRAM_ID")
PAGE_ID = os.getenv("PAGE_ID")

# Define limite de data (D-1)
limite_data = datetime.now(timezone.utc) - timedelta(days=1)

def deletar_post(post_id, plataforma, index):
    url = f"https://graph.facebook.com/v19.0/{post_id}"
    res = requests.delete(url, params={"access_token": ACCESS_TOKEN})
    if res.status_code == 200:
        print(f"✅ [{plataforma}] Postagem {index} deletada com sucesso: {post_id}")
    else:
        print(f"❌ [{plataforma}] Falha ao deletar {post_id}: {res.text}")

# --- Facebook ---
def deletar_feed_facebook():
    print("📘 Buscando posts no Facebook...")
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/posts"
    params = {"access_token": ACCESS_TOKEN, "fields": "id,created_time", "limit": 100}
    res = requests.get(url, params=params)
    data = res.json().get("data", [])

    for i, post in enumerate(data, 1):
        data_post = datetime.fromisoformat(post["created_time"].replace("Z", "+00:00"))
        if data_post <= limite_data:
            deletar_post(post["id"], "Facebook", i)

# --- Instagram ---
def deletar_feed_instagram():
    print("📸 Buscando posts no Instagram...")
    url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_ID}/media"
    params = {"access_token": ACCESS_TOKEN, "fields": "id,timestamp", "limit": 100}
    res = requests.get(url, params=params)
    data = res.json().get("data", [])

    for i, post in enumerate(data, 1):
        data_post = datetime.fromisoformat(post["timestamp"].replace("Z", "+00:00"))
        if data_post <= limite_data:
            deletar_post(post["id"], "Instagram", i)

if __name__ == "__main__":
    deletar_feed_facebook()
    deletar_feed_instagram()
    print("🏁 Deleção concluída.")
