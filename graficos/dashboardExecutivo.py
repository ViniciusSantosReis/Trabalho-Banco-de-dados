import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DW_USER')}:{os.getenv('DW_PASSWORD')}@{os.getenv('DW_HOST')}:{os.getenv('DW_PORT')}/{os.getenv('DW_NAME')}"
)

query = """
SELECT 
    valor_convertido,
    quantidade_transacionada
FROM fato_transacoes_internacionais
"""

df = pd.read_sql(query, engine)

# KPIs
valor_total = df["valor_convertido"].sum()
quantidade_total = df["quantidade_transacionada"].sum()
total_transacoes = len(df)
ticket_medio = valor_total / total_transacoes

# DASHBOARD

fig, axs = plt.subplots(2, 2, figsize=(12, 7))

fig.patch.set_facecolor("#0f172a")  # azul escuro


def criar_card(ax, titulo, valor):
    ax.set_facecolor("#1e293b")  # fundo do card
    ax.set_xticks([])
    ax.set_yticks([])

    # borda arredondada (simulada)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.text(0.5, 0.65, titulo,
            ha='center', va='center',
            fontsize=12, color="#94a3b8")

    ax.text(0.5, 0.35, valor,
            ha='center', va='center',
            fontsize=18, color="#f8fafc", weight='bold')


# cards
criar_card(axs[0, 0], "Valor Total", f"R$ {valor_total:,.2f}")
criar_card(axs[0, 1], "Quantidade Total", f"{quantidade_total:,.0f}")
criar_card(axs[1, 0], "Total de Transações", f"{total_transacoes:,.0f}")
criar_card(axs[1, 1], "Ticket Médio", f"R$ {ticket_medio:,.2f}")

# título geral
plt.suptitle("Painel Executivo - Operações Internacionais",
             fontsize=18, color="white", y=0.98)

plt.tight_layout()
plt.show()