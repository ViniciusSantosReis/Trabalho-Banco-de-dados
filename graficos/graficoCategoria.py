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
    dp.categoria_produto,
    SUM(f.valor_convertido) AS total_valor
FROM fato_transacoes_internacionais f
JOIN dim_produto dp ON f.sk_produto = dp.sk_produto
GROUP BY dp.categoria_produto
ORDER BY total_valor DESC;
"""

df_categoria= pd.read_sql(query, engine)

df_categoria["total_valor"] = df_categoria["total_valor"] / 1_000_000

df_categoria = df_categoria.sort_values("total_valor", ascending=True)

plt.figure()

plt.barh(df_categoria["categoria_produto"], df_categoria["total_valor"])

plt.title("Valor Total por Categoria de Produto")
plt.xlabel("Valor Total (milhões)")
plt.ylabel("Categoria")

plt.tight_layout()
plt.show()