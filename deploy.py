import os
import subprocess
try:
    print("🛍️ Gerando loja HTML...")
    subprocess.run(["python", "scripts/gerar_loja_html.py"], check=True)
except subprocess.CalledProcessError as e:
    print("❌ Erro ao gerar HTML:", e)
    exit(1)

# Etapa 4: Commit e push automático para o repositório (branch master)
try:
    print("📦 Fazendo commit e push das alterações...")
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "🚀 Atualização automática via pipeline"], check=True)
    subprocess.run(["git", "push", "origin", "master"], check=True)
    print("✅ Código enviado com sucesso ao repositório remoto.")
except subprocess.CalledProcessError as e:
    print("⚠️ Erro ao fazer commit ou push:", e)

print("\n✅ Pipeline executado com sucesso!")