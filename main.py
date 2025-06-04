# main.py
import os
import subprocess

print("\n🚀 Iniciando pipeline...")

# Executa o coletor da Shopee
try:
    print("🔎 Coletando produtos da Shopee...")
    subprocess.run(["python", "api/shopee.py"], check=True)
except subprocess.CalledProcessError as e:
    print("❌ Erro ao coletar dados da Shopee:", e)
    exit(1)

# Executa o publicador
try:
    print("📤 Publicando produto no Facebook...")
    subprocess.run(["python", "scripts/publicar_hoje.py"], check=True)
except subprocess.CalledProcessError as e:
    print("❌ Erro ao publicar:", e)
    exit(1)

try:
    # Depois de publicar no Facebook
    print("🛍️ Gerando loja HTML...")
    subprocess.run(["python", "scripts/gerar_loja_html.py"])

except subprocess.CalledProcessError as e:
    print("❌ Erro ao gerar HTML c:", e)
    exit(1)

print("\n✅ Pipeline executado com sucesso!")
