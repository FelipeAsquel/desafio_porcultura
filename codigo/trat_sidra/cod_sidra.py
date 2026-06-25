import pandas as pd
import os
import csv

anos = range(2017, 2025)

culturas = [
    "arroz",
    "batata_inglesa",
    "cebola",
    "cevada",
    "feijao",
    "milho",
    "soja",
    "trigo"
]

pasta_entrada = "da_brutos"
pasta_saida = "da_tratados"

os.makedirs(pasta_saida, exist_ok=True)

nomes_culturas = {
    "arroz": "Arroz",
    "batata_inglesa": "Batata_inglesa",
    "cebola": "Cebola",
    "cevada": "Cevada",
    "feijao": "Feijao",
    "milho": "Milho",
    "soja": "Soja",
    "trigo": "Trigo"
}


def pegar_variavel(texto):
    texto = texto.replace('"', "").strip()

    if not texto.startswith("Variável -"):
        return None

    if "Área plantada" in texto:
        return "Area_Plantada"
    elif "Área colhida" in texto:
        return "Area_Colhida"
    elif "Quantidade produzida" in texto:
        return "Producao_Ton"
    elif "Rendimento médio" in texto or "Rendimento" in texto:
        return "Rendimento"
    elif "Valor da produção" in texto:
        return "Valor"

    return None


def ajustar_valor(valor):
    valor = str(valor).strip().replace('"', "")

    if valor in ["-", "...", "X", "x", "", "nan", "None"]:
        return pd.NA

    return valor


def tratar_arquivo(caminho, ano, cultura):
    dados = []
    variavel_atual = None

    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")

        for linha in leitor:
            if len(linha) == 0:
                continue

            variavel = pegar_variavel(linha[0])

            if variavel is not None:
                variavel_atual = variavel
                continue

            if variavel_atual is None or len(linha) < 4:
                continue

            nivel = linha[0].strip().replace('"', "")

            if nivel != "MU":
                continue

            codigo = linha[1].strip().replace('"', "")
            municipio = linha[2].strip().replace('"', "")
            valor = ajustar_valor(linha[3])

            dados.append({
                "COD_IBGE": codigo,
                "Municipio": municipio,
                "Variavel": variavel_atual,
                "Valor": valor
            })

    df = pd.DataFrame(dados)

    if df.empty:
        return pd.DataFrame()

    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    df["UF"] = df["Municipio"].str.extract(r"\(([A-Z]{2})\)")

    df["Municipio"] = df["Municipio"].str.replace(
        r"\s*\([A-Z]{2})\)$",
        "",
        regex=True
    )

    tabela = df.pivot_table(
        index=["COD_IBGE", "Municipio", "UF"],
        columns="Variavel",
        values="Valor",
        aggfunc="first"
    ).reset_index()

    tabela.columns.name = None

    tabela["Ano"] = ano
    tabela["Cultura"] = nomes_culturas[cultura]

    colunas = [
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

    for coluna in colunas:
        if coluna not in tabela.columns:
            tabela[coluna] = pd.NA

    return tabela[colunas]


for ano in anos:
    pasta_ano = os.path.join(pasta_entrada, str(ano))
    saida_ano = os.path.join(pasta_saida, str(ano))

    os.makedirs(saida_ano, exist_ok=True)

    for cultura in culturas:
        caminho = os.path.join(pasta_ano, f"{cultura}.csv")

        if not os.path.exists(caminho):
            continue

        df_final = tratar_arquivo(caminho, ano, cultura)

        if df_final.empty:
            continue

        saida = os.path.join(saida_ano, f"{cultura}_{ano}.csv")

        df_final.to_csv(
            saida,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"{cultura}_{ano}.csv salvo")


