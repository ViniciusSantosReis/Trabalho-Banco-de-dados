import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DW_USER')}:{os.getenv('DW_PASSWORD')}@{os.getenv('DW_HOST')}:{os.getenv('DW_PORT')}/{os.getenv('DW_NAME')}"
)

query = """
SELECT 
    p.pais,
    SUM(f.valor_convertido) AS total_valor
FROM fato_transacoes_internacionais f
JOIN dim_pais p ON f.sk_pais_destino = p.sk_pais
GROUP BY p.pais
ORDER BY total_valor DESC
LIMIT 10;
"""

df_destino = pd.read_sql(query, engine)

df_destino["total_valor"] = df_destino["total_valor"] / 1_000_000

df_destino = df_destino.sort_values("total_valor", ascending=True)

plt.figure()

plt.barh(df_destino["pais"], df_destino["total_valor"])

plt.title("Top 10 Países de Destino (Importações)")
plt.xlabel("Valor Total (milhões)")
plt.ylabel("País")

plt.tight_layout()
plt.show()