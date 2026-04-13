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
    ROUND(f.taxa_cambio_aplicada, 2) AS taxa_cambio,
    SUM(f.valor_convertido) AS total_valor
FROM fato_transacoes_internacionais f
GROUP BY taxa_cambio
ORDER BY taxa_cambio;
"""

df_cambio = pd.read_sql(query, engine)

df_cambio["total_valor"] = df_cambio["total_valor"] / 1_000_000

plt.figure(figsize=(10,6))

plt.scatter(df_cambio["taxa_cambio"], df_cambio["total_valor"])

plt.title("Impacto da Taxa de Câmbio nas Transações")
plt.xlabel("Taxa de Câmbio")
plt.ylabel("Valor da Transação")

plt.show()