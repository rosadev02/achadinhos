import pandas as pd
import os

TEMPLATE_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Achadinhos do Dia 🛍️</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #fafafa;
            margin: 0;
            padding: 20px;
            text-align: center;
        }}
        h1 {{
            color: #6a1b9a;
        }}
        .grid {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }}
        .produto {{
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            width: 260px;
            padding: 10px;
            text-align: center;
        }}
        .produto img {{
            width: 100%;
            height: auto;
            border-radius: 6px;
        }}
        .produto h3 {{
            font-size: 16px;
            color: #333;
        }}
        .produto p {{
            font-size: 14px;
            color: #777;
        }}
        .produto a {{
            background: #8e24aa;
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            text-decoration: none;
            display: inline-block;
            margin-top: 8px;
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
