import requests

# Substitua aqui com seus dados reais:
PAGE_ID = "637917292744635"
ACCESS_TOKEN = "EAAsdCgExOnoBO7qGyq8gYZBOa732VhgXX1FYKZC1KhInZCB9llF2zF7nJPLNzKQv2vSWazpTXGUOVeKS4RcSWGmz6uGOebgb5d3836gRKZBHNJdcQRNa8rztMM1fveCGYX7PTWI7wtjSpIF74u3KUIpcrZAHOmj7Q7fNK91gYUdLofyZAPVSVCk2qLDxU7vTsI2hM2wDmA4T3nW6YaCUYi6uqFnlPRklbpzSGhpR4hoJQUUVAR"

# Mensagem a ser publicada
mensagem = "🚨 Oferta do dia! Promoções validadas por IA! Acesse nosso perfil e aproveite. 🤖🛍️"

# Endpoint da API do Facebook
url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"

# Parâmetros da requisição
params = {
    "message": mensagem,
    "access_token": ACCESS_TOKEN
}

# Enviar requisição POST
resposta = requests.post(url, data=params)

# Resultado
if resposta.status_code == 200:
    print("✅ Post publicado com sucesso!")
    print("ID do post:", resposta.json()["id"])
else:
    print("❌ Erro ao publicar o post.")
    print("Status:", resposta.status_code)
    print("Resposta:", resposta.text)