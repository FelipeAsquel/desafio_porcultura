import pandas as pd
import os

pasta_tratados = "da_tratados"
pasta_saida = "basefinal"
saida = os.path.join(pasta_saida, "base_pam_sidra_2009_2024.csv")

os.makedirs(pasta_saida, exist_ok=True)

colunas_finais = [
    "Ano",
    "Cultura",
    "UF",
    "Municipio",
    "COD_IBGE",
    "Area_Plantada",
    "Area_Colhida",
    "Producao_Ton",
    "Rendimento",
    "Valor"
]

colunas_numericas = [
    "Area_Plantada",
    "Area_Colhida",
    "Producao_Ton",
    "Rendimento",
    "Valor"
]

bases = []

for ano in os.listdir(pasta_tratados):
    caminho_ano = os.path.join(pasta_tratados, ano)

    if not os.path.isdir(caminho_ano):
        continue

    for arquivo in os.listdir(caminho_ano):
        if arquivo.endswith(".csv") and "_sem_codigo" not in arquivo:
            caminho = os.path.join(caminho_ano, arquivo)

            df = pd.read_csv(caminho, encoding="utf-8-sig")

            df = df[colunas_finais]

            bases.append(df)

base_final = pd.concat(bases, ignore_index=True)

for coluna in colunas_numericas:
    base_final[coluna] = (
        base_final[coluna]
        .astype(str)
        .str.strip()
        .replace({
            "-": pd.NA,
            "...": pd.NA,
            "X": pd.NA,
            "x": pd.NA,
            "nan": pd.NA,
            "None": pd.NA,
            "": pd.NA
        })
    )

    base_final[coluna] = pd.to_numeric(base_final[coluna], errors="coerce")

base_final["Ano"] = pd.to_numeric(
    base_final["Ano"],
    errors="coerce"
).astype("Int64")

base_final["COD_IBGE"] = (
    base_final["COD_IBGE"]
    .astype(str)
    .str.replace(r"\.0$", "", regex=True)
)

base_final.to_csv(saida, index=False, encoding="utf-8-sig")

print("Base final criada.")
print(base_final.shape)

print("\nAnos:")
print(sorted(base_final["Ano"].dropna().unique()))

print("\nCulturas:")
print(sorted(base_final["Cultura"].dropna().unique()))

print("\nValores vazios:")
print(base_final.isna().sum())