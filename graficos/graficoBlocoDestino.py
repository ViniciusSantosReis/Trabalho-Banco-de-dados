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
    p.bloco_economico,
    SUM(f.valor_convertido) AS total_valor
FROM fato_transacoes_internacionais f
JOIN dim_pais p ON f.sk_pais_destino = p.sk_pais
GROUP BY p.bloco_economico
ORDER BY total_valor DESC;
"""

df_bloco = pd.read_sql(query, engine)

df_bloco["total_valor"] = df_bloco["total_valor"] / 1_000_000

df_bloco = df_bloco.sort_values("total_valor", ascending=True)

plt.figure()

plt.barh(df_bloco["bloco_economico"], df_bloco["total_valor"])

plt.title("Valor Total por Bloco Econômico (Destino)")
plt.xlabel("Valor Total (milhões)")
plt.ylabel("Bloco Econômico")

plt.tight_layout()
plt.show()