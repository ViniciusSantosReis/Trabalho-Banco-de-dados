import mysql.connector
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()

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

print(df.head())
print(df.columns)

