import pandas as pd
import os

TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Achadinhos do Dia 🛍️</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(to bottom right, #f3e5f5, #ede7f6);
            margin: 0;
            padding: 30px 20px;
        }}
        h1 {{
            color: #6a1b9a;
            text-align: center;
            margin-bottom: 40px;
            font-size: 32px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 25px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .produto {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
            overflow: hidden;
            transition: transform 0.2s;
        }}
        .produto:hover {{
            transform: translateY(-5px);
        }}
        .produto img {{
            width: 100%;
            height: 240px;
            object-fit: cover;
        }}
        .produto h3 {{
            font-size: 16px;
            color: #333;
            padding: 15px 12px 5px;
            height: 48px;
            overflow: hidden;
        }}
        .produto p {{
            font-size: 15px;
            color: #6a1b9a;
            font-weight: bold;
            padding: 0 12px;
        }}
        .produto a {{
            display: block;
            margin: 12px;
            padding: 10px;
            background-color: #8e24aa;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: background-color 0.2s;
        }}
        .produto a:hover {{
            background-color: #6a1b9a;
        }}
    </style>
</head>
<body>
    <h1>Achadinhos do Dia 💜</h1>
    <div class="grid">
        {produtos}
    </div>
</body>
</html>
"""


def gerar_card(produto):
    return f"""
    <div class="produto">
        <img src="{produto['imageUrl']}" alt="{produto['productName']}">
        <h3>{produto['productName'][:70]}</h3>
        <p>R$ {produto['price']}</p>
        <a href="{produto['offerLink']}" target="_blank">Ver Oferta</a>
    </div>
    """

def gerar_loja_html(csv_path, output_path="static/index.html", limite=30):
    df = pd.read_csv(csv_path)
    produtos = "\n".join([gerar_card(row) for _, row in df.head(limite).iterrows()])
    html = TEMPLATE_HTML.format(produtos=produtos)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Loja HTML gerada em {output_path}")

if __name__ == "__main__":
    gerar_loja_html("data/ofertas_shopee.csv")
