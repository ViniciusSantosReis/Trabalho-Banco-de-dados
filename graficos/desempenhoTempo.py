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
    dt.ano,
    dt.mes,
    SUM(f.valor_convertido) AS total_valor
FROM fato_transacoes_internacionais f
JOIN dim_tempo dt ON f.sk_tempo = dt.sk_tempo
GROUP BY dt.ano, dt.mes
ORDER BY dt.ano, dt.mes;
"""

df_tempo = pd.read_sql(query, engine)

df_tempo["data"] = pd.to_datetime(
    df_tempo["ano"].astype(str) + "-" + df_tempo["mes"].astype(str) + "-01"
)

df_tempo["total_valor"] = df_tempo["total_valor"] / 1_000_000

plt.figure()

plt.plot(df_tempo["data"], df_tempo["total_valor"])

plt.title("Volume Financeiro das Transações ao Longo do Tempo")
plt.xlabel("Tempo")
plt.ylabel("Valor Total (Em Milhões)")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()