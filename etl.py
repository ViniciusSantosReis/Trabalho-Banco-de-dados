import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sqlalchemy import create_engine
from sqlalchemy import text

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(
    f"mysql+pymysql://{os.getenv('DW_USER')}:{os.getenv('DW_PASSWORD')}@{os.getenv('DW_HOST')}:{os.getenv('DW_PORT')}/{os.getenv('DW_NAME')}"
)

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

print("Conectado com sucesso!")

query = """
SELECT
    t.id,
    t.valor_monetario as valor_original,
    t.quantidade,

    -- tempo
    c.data,

    -- produto
    p.descricao as produto,
    cp.descricao as categoria_produto,
    p.codigo_ncm as ncm_produto,

    -- país origem
    po.nome as pais_origem,
    po.codigo_iso as cod_iso_origem,
    bo.nome as bloco_origem,

    -- país destino
    pd.nome as pais_destino,
    pd.codigo_iso as cod_iso_destino,
    bd.nome as bloco_destino,

    -- moeda origem
    m1.descricao as moeda_origem,
    m1.pais as pais_moeda_origem,
    
    -- moeda destino
    m2.descricao as moeda_destino,
	m2.pais as pais_moeda_destino,
    
    -- taxa
    c.taxa_cambio,
    
    -- transporte
    tr.descricao as transporte,
    
    -- tipo
    tip.descricao as tipo_transacao

FROM transacoes t

JOIN cambios c ON t.cambio_id = c.id
JOIN produtos p ON t.produto_id = p.id
JOIN paises po on t.pais_origem = po.id
JOIN paises pd on t.pais_destino = pd.id
JOIN transportes tr on t.transporte_id = tr.id
JOIN tipos_transacoes tip on t.tipo_id = tip.id
JOIN moedas m1 ON c.moeda_origem = m1.id
JOIN moedas m2 ON c.moeda_destino = m2.id
JOIN blocos_economicos bo ON po.bloco_id = bo.id
JOIN blocos_economicos bd ON pd.bloco_id = bd.id
JOIN categoria_produtos cp ON p.categoria_id = cp.id

order by t.id
"""

def padronizar_texto(col):
    return col.str.strip().str.title()

df = pd.read_sql(query, conn)

df["data"] = pd.to_datetime(df["data"])

df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month
df["dia"] = df["data"].dt.day
df["dia_semana"] = df["data"].dt.day_name()

df["valor_convertido"] = df["valor_original"] * df["taxa_cambio"]

#Padronização do df
df["produto"] = padronizar_texto(df["produto"])
df["categoria_produto"] = padronizar_texto(df["categoria_produto"])
df["ncm_produto"] = df["ncm_produto"].str.strip()
df["pais_origem"] = padronizar_texto(df["pais_origem"])
df["bloco_origem"] = padronizar_texto(df["bloco_origem"])
df["pais_destino"] = padronizar_texto(df["pais_destino"])
df["bloco_destino"] = padronizar_texto(df["bloco_destino"])
df["cod_iso_origem"] = df["cod_iso_origem"].str.strip().str.upper()
df["cod_iso_destino"] = df["cod_iso_destino"].str.strip().str.upper()
df["tipo_transacao"] = padronizar_texto(df["tipo_transacao"])
df["transporte"] = padronizar_texto(df["transporte"])
df["moeda_origem"] = padronizar_texto(df["moeda_origem"])
df["pais_moeda_origem"] = padronizar_texto(df["pais_moeda_origem"])
df["moeda_destino"] = padronizar_texto(df["moeda_destino"])
df["pais_moeda_destino"] = padronizar_texto(df["pais_moeda_destino"])
df["transporte"] = padronizar_texto(df["transporte"])
df["tipo_transacao"] = padronizar_texto(df["tipo_transacao"])
df["moeda_origem"] = padronizar_texto(df["moeda_origem"])
df["moeda_destino"] = padronizar_texto(df["moeda_destino"])


# Dimensão Tempo
dim_tempo = df[["data"]].drop_duplicates().copy()



dim_tempo["dia"] = dim_tempo["data"].dt.day
dim_tempo["mes"] = dim_tempo["data"].dt.month
dim_tempo["nome_mes"] = dim_tempo["data"].dt.month_name()
dim_tempo["trimestre"] = dim_tempo["data"].dt.quarter
dim_tempo["semestre"] = dim_tempo["mes"].apply(lambda x: 1 if x <= 6 else 2)
dim_tempo["ano"] = dim_tempo["data"].dt.year
dim_tempo["dia_da_semana"] = dim_tempo["data"].dt.day_name()

# Criando surrogate key
dim_tempo = dim_tempo.sort_values("data").reset_index(drop=True)
dim_tempo["sk_tempo"] = range(1, len(dim_tempo) + 1)

# Organizando Colunas
dim_tempo = dim_tempo[
    ["sk_tempo", "data", "dia", "mes", "nome_mes", "trimestre", "semestre", "ano", "dia_da_semana"]
]

# Ligando dimensão tempo com tabela fato (pela SK)
df = df.merge(
    dim_tempo[["data", "sk_tempo"]],
    on="data",
    how="left"
)

# Dimensão Produto
dim_produto = df[["produto", "categoria_produto", "ncm_produto"]].copy()

dim_produto = dim_produto.drop_duplicates()

dim_produto = dim_produto.reset_index(drop=True)
dim_produto["sk_produto"] = range(1, len(dim_produto)+1)
dim_produto = dim_produto[
    ["sk_produto","produto", "categoria_produto", "ncm_produto"]
]

# Mapeando SK de produto na fato
df = df.merge(
    dim_produto,
    on=["produto", "categoria_produto", "ncm_produto"],
    how="left"
)

# Criando Dimensão País
df_origem = df[["pais_origem", "cod_iso_origem", "bloco_origem"]].drop_duplicates().copy()
df_origem.columns = ["pais", "cod_iso", "bloco_economico"]

df_destino = df[["pais_destino", "cod_iso_destino", "bloco_destino"]].drop_duplicates().copy()
df_destino.columns = ["pais", "cod_iso", "bloco_economico"]

df_origem = df_origem.reset_index(drop=True)
df_destino = df_destino.reset_index(drop=True)

dim_pais = pd.concat([df_origem, df_destino])
dim_pais = dim_pais.drop_duplicates()
dim_pais = dim_pais.reset_index(drop=True)

dim_pais["sk_pais"] = range(1, len(dim_pais) + 1)
dim_pais = dim_pais[["sk_pais", "pais", "cod_iso", "bloco_economico"]]

# Mapeando SKs de pais na fato
# Lefton = df RightOn = dimensão
df = df.merge(
    dim_pais,
    left_on="pais_origem",
    right_on="pais",
    how="left"
)

df.rename(columns={'sk_pais': 'sk_pais_origem'}, inplace=True)
df = df.drop(columns=["pais", "cod_iso", "bloco_economico"])

df = df.merge(
    dim_pais,
    left_on="pais_destino",
    right_on="pais",
    how="left"
)

df.rename(columns={'sk_pais': 'sk_pais_destino'}, inplace=True)
df = df.drop(columns=["pais", "cod_iso", "bloco_economico"])


df = df.drop(columns=["produto", "categoria_produto", "ncm_produto"])

#dimensao tipo transacao
dim_tipo_transacao = df[["tipo_transacao"]].drop_duplicates().copy()
dim_tipo_transacao["tipo_transacao"] = padronizar_texto(dim_tipo_transacao["tipo_transacao"])

# surrogate key
dim_tipo_transacao = dim_tipo_transacao.reset_index(drop=True)
dim_tipo_transacao["sk_tipo_transacao"] = range(1, len(dim_tipo_transacao) + 1)

#renomear coluna
dim_tipo_transacao.rename(columns={"tipo_transacao": "descricao_tipo_transacao"},inplace=True)




#mapear tabela fato
df = df.merge(
    dim_tipo_transacao,
    left_on="tipo_transacao",
    right_on="descricao_tipo_transacao",
    how="left"

)

df = df.drop(columns=["tipo_transacao", "descricao_tipo_transacao"])



#dminesao transporte
dim_transporte = df[["transporte"]].drop_duplicates().copy()

#surrogate key
dim_transporte = dim_transporte.reset_index(drop=True)
dim_transporte["sk_transporte"] = range(1, len(dim_transporte) + 1)

#renomear coluna
dim_transporte.rename(columns={"transporte": "descricao_transporte"},inplace=True)

dim_transporte = dim_transporte[["sk_transporte", "descricao_transporte"]]

df = df.merge(
    dim_transporte,
    left_on="transporte",
    right_on="descricao_transporte",
    how="left"
)

df = df.drop(columns=["transporte", "descricao_transporte"])


#dimensao moeda
df_moeda_origem = df[["moeda_origem", "pais_moeda_origem"]].drop_duplicates().copy()
df_moeda_origem.columns = ["descricao_moeda", "pais_moeda"]

df_moeda_destino = df[["moeda_destino", "pais_moeda_destino"]].drop_duplicates().copy()
df_moeda_destino.columns = ["descricao_moeda", "pais_moeda"]


#dimensao unica e SK
dim_moeda = pd.concat([df_moeda_origem, df_moeda_destino]).drop_duplicates().reset_index(drop=True)
dim_moeda["sk_moeda"] = range(1, len(dim_moeda) + 1)
dim_moeda = dim_moeda[["sk_moeda", "descricao_moeda", "pais_moeda"]]

# Mapeando SKs de moeda na fato
df = df.merge(
    dim_moeda,
    left_on=["moeda_origem","pais_moeda_origem"],
    right_on=["descricao_moeda", "pais_moeda"],
    how="left"
)

df.rename(columns={"sk_moeda": "sk_moeda_origem"},inplace=True)
df = df.drop(columns=["descricao_moeda", "pais_moeda"])


df = df.merge(
    dim_moeda,
    left_on=["moeda_destino","pais_moeda_destino"],
    right_on=["descricao_moeda", "pais_moeda"],
    how="left"
)

df.rename(columns={"sk_moeda": "sk_moeda_destino"},inplace=True)
df = df.drop(columns=["descricao_moeda", "pais_moeda"])

df = df.drop(columns=["moeda_origem", "pais_moeda_origem", "moeda_destino", "pais_moeda_destino", "ano", "mes", "dia", "dia_semana"])
df = df.drop(columns=["data", "pais_origem", "pais_destino","cod_iso_origem","cod_iso_destino","bloco_origem","bloco_destino",])

# Organizando
fato = df[[
    "sk_tempo",
    "sk_produto",
    "sk_pais_origem",
    "sk_pais_destino",
    "sk_moeda_origem",
    "sk_moeda_destino",
    "sk_transporte",
    "sk_tipo_transacao",
    "quantidade",
    "valor_original",
    "valor_convertido",
    "taxa_cambio"
]].copy()

fato.rename(columns={
    "quantidade": "quantidade_transacionada",
    "valor_original": "valor_transacao",
    "taxa_cambio": "taxa_cambio_aplicada"
}, inplace=True)




# CARGA
def limpar_DW(engine):
    with engine.connect() as conn:
        print("executando limpeza")

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        conn.execute(text("TRUNCATE TABLE fato_transacoes_internacionais"))
        conn.execute(text("TRUNCATE TABLE dim_tempo"))
        conn.execute(text("TRUNCATE TABLE dim_produto"))
        conn.execute(text("TRUNCATE TABLE dim_pais"))
        conn.execute(text("TRUNCATE TABLE dim_moeda"))
        conn.execute(text("TRUNCATE TABLE dim_transporte"))
        conn.execute(text("TRUNCATE TABLE dim_tipo_transacao"))

        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        conn.commit()

print("Iniciando carga no DW...")

print("executando limpeza")
limpar_DW(engine)

print("Carregando dim_tempo...")
dim_tempo.to_sql("dim_tempo", engine, if_exists="append", index=False)

print("Carregando dim_produto...")
dim_produto.to_sql("dim_produto", engine, if_exists="append", index=False)

print("Carregando dim_pais...")
dim_pais.to_sql("dim_pais", engine, if_exists="append", index=False)

print("Carregando dim_tipo_transacao...")
dim_tipo_transacao.to_sql("dim_tipo_transacao", engine, if_exists="append", index=False)

print("Carregando dim_transporte...")
dim_transporte.to_sql("dim_transporte", engine, if_exists="append", index=False)

print("Carregando dim_moeda...")
dim_moeda.to_sql("dim_moeda", engine, if_exists="append", index=False)

# ==============================
# CARGA FATO
# ==============================

print("Carregando fato...")
fato.to_sql("fato_transacoes_internacionais", engine, if_exists="append", index=False)

print("✅ Carga finalizada com sucesso!")