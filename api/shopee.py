import os
import time
import hashlib
import requests
import json
import pandas as pd

APP_ID = os.getenv("APP_ID") or "18315210384"
APP_SECRET = os.getenv("APP_SECRET") or "W4DNCZTB2VEGIXY5IIVLU6P33SVT3DEF"

MAX_PAGINAS = 3  # ← ALTERE AQUI o número máximo de páginas a coletar

def gerar_signature(app_id, timestamp, payload_str, secret):
    base = app_id + str(timestamp) + payload_str + secret
    return hashlib.sha256(base.encode()).hexdigest()

def coletar_ofertas():
    url = "https://open-api.affiliate.shopee.com.br/graphql"
    scroll_id = ""
    todos_produtos = []
    pagina_atual = 1

    while pagina_atual <= MAX_PAGINAS:
        query_str = f"""
        {{
            productOfferV2({f'scrollId: "{scroll_id}"' if scroll_id else ""}) {{
                nodes {{
                    productName
                    itemId
                    commissionRate
                    commission
                    price
                    sales
                    imageUrl
                    shopName
                    productLink
                    offerLink
                    ratingStar
                }}
                pageInfo {{
                    hasNextPage
                    scrollId
                }}
            }}
        }}
        """

        payload = {"query": query_str}
        payload_str = json.dumps(payload, separators=(',', ':'))
        timestamp = int(time.time())
        signature = gerar_signature(APP_ID, timestamp, payload_str, APP_SECRET)

        headers = {
            "Authorization": f"SHA256 Credential={APP_ID}, Timestamp={timestamp}, Signature={signature}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, data=payload_str)

        if response.status_code != 200:
            raise Exception(f"Erro na requisição: {response.status_code}\n{response.text}")

        json_data = response.json()
        data = json_data["data"]["productOfferV2"]
        todos_produtos.extend(data["nodes"])

        print(f"✅ Página {pagina_atual} coletada com sucesso.")

        if not data["pageInfo"]["hasNextPage"]:
            break

        scroll_id = data["pageInfo"]["scrollId"]
        pagina_atual += 1

    return {"nodes": todos_produtos}

def salvar_csv(produtos, path="data/ofertas_shopee.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df = pd.DataFrame(produtos)
    df.to_csv(path, index=False)
    print(f"✅ Arquivo salvo em {path}")

if __name__ == "__main__":
    print("🔎 Coletando produtos da Shopee...")
    try:
        resultado = coletar_ofertas()
        salvar_csv(resultado["nodes"])
    except Exception as e:
        print("❌ Erro ao coletar dados da Shopee:", e)
