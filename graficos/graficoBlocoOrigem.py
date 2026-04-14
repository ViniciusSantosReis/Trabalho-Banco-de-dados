import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DW_USER')}:{os.getenv('DW_PASSWORD')}@{os.getenv('DW_HOST')}:{os.getenv('DW_PORT')}/{os.getenv('DW_NAME')}"
)

query = """
SELECT 
    p.bloco_economico,
    SUM(f.valor_convertido) AS total_valor
FROM fato_transacoes_internacionais f
JOIN dim_pais p ON f.sk_pais_origem = p.sk_pais
GROUP BY p.bloco_economico
ORDER BY total_valor DESC;
"""

df_bloco = pd.read_sql(query, engine)

plt.figure(figsize=(8,8))

plt.pie(
    df_bloco["total_valor"],
    labels=df_bloco["bloco_economico"],
    autopct='%1.1f%%',
    startangle=140,
    wedgeprops={'edgecolor': 'white'}
)

plt.title("Participação por Bloco Econômico (Origem)", fontsize=14)

plt.tight_layout()
plt.show()