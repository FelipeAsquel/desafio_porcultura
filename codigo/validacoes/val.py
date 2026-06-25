import pandas as pd

caminho = r"basefinal\base_pam_sidra_2009_2024.csv"

# lê a base final
df = pd.read_csv(caminho, encoding="utf-8-sig")

# colunas que serão usadas como número
colunas_numericas = [
    "Area_Plantada",
    "Area_Colhida",
    "Producao_Ton",
    "Rendimento",
    "Valor"
]

# mostra o tamanho da tabela: linhas e colunas
print("Formato da base:")
print(df.shape)

# mostra as primeiras linhas para conferir se a leitura deu certo
print("\nPrimeiras linhas:")
print(df.head())

# mostra quais anos e culturas aparecem na base
print("\nAnos:")
print(sorted(df["Ano"].unique()))

print("\nCulturas:")
print(sorted(df["Cultura"].unique()))

# confere se existem valores vazios nas colunas
print("\nValores vazios:")
print(df.isna().sum())

# transforma as colunas principais em valores numéricos
# se algum valor não virar número, ele vira vazio
for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# verifica se existe linha repetida para o mesmo ano, cultura e município
print("\nDuplicados por ano, cultura e município:")
duplicados = df.duplicated(
    subset=["Ano", "Cultura", "COD_IBGE"]
).sum()

print(duplicados)


# soma a produção por ano
print("\nProdução total por ano:")
print(df.groupby("Ano")["Producao_Ton"].sum().sort_index())

# soma a produção por cultura
print("\nProdução total por cultura:")
print(df.groupby("Cultura")["Producao_Ton"].sum().sort_values(ascending=False))

# soma a produção por estado
print("\nProdução total por UF:")
print(df.groupby("UF")["Producao_Ton"].sum().sort_values(ascending=False))
