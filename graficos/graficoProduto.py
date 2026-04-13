import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DW_USER')}:{os.getenv('DW_PASSWORD')}@{os.getenv('DW_HOST')}:{os.getenv('DW_PORT')}/dw_comex"
)

query = """
SELECT 
    dp.produto,
    SUM(f.valor_convertido) as total_valor
FROM fato_transacoes_internacionais f
JOIN dim_produto dp ON f.sk_produto = dp.sk_produto
GROUP BY dp.produto
ORDER BY total_valor DESC
LIMIT 10
"""

df_grafico = pd.read_sql(query, engine)
df_grafico["total_valor"] = df_grafico["total_valor"] / 1_000_000

plt.figure()

plt.barh(df_grafico["produto"], df_grafico["total_valor"])

plt.title("Top 10 Produtos por Valor Total", fontsize=14)
plt.xlabel("Valor (em milhões)")
plt.ylabel("Produto")

plt.tight_layout()
plt.show()