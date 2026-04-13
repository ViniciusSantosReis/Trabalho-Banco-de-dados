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
    p.pais,
    SUM(f.valor_convertido) AS total_valor
FROM fato_transacoes_internacionais f
JOIN dim_pais p ON f.sk_pais_origem = p.sk_pais
GROUP BY p.pais
ORDER BY total_valor DESC
LIMIT 10;
"""

df_origem= pd.read_sql(query, engine)

df_origem["total_valor"] = df_origem["total_valor"] / 1_000_000

df_origem = df_origem.sort_values("total_valor", ascending=True)

plt.figure()

plt.barh(df_origem["pais"], df_origem["total_valor"])

plt.title("Top 10 Países de Origem (Exportações)")
plt.xlabel("Valor Total (milhões)")
plt.ylabel("País")

plt.tight_layout()
plt.show()