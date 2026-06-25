import pandas as pd
import xlrd
import os
from dic import *


def tratamento(ano):
    pasta_entrada = f"da_brutos/{ano}"
    pasta_saida = f"da_tratados/{ano}"

    os.makedirs(pasta_saida, exist_ok=True)


    for arquivo in os.listdir(pasta_saida):
        if arquivo.endswith("_sem_codigo.csv"):
            os.remove(os.path.join(pasta_saida, arquivo))

    ano_geo = ano_municipio(ano)

    municipios_ibge = pd.read_csv(
        rf"da_geo\{ano_geo}\municipios_ibge_{ano_geo}.csv",
        encoding="utf-8-sig"
    )

    correcoes = CORRECOES[str(ano)]

    municipios_ibge["Municipio_limpo"] = municipios_ibge["MUNICIPIO"].apply(limpar_texto)

    for arquivo_nome in os.listdir(pasta_entrada):

        if not arquivo_nome.endswith(".xls"):
            continue

        caminho = os.path.join(pasta_entrada, arquivo_nome)
        cultura = arquivo_nome.replace(".xls", "").capitalize()

        wb = xlrd.open_workbook(caminho, formatting_info=True)
        ws = wb.sheet_by_index(0)

        dados = []
        estado_atual = None

        for i in range(6, ws.nrows):
            nome = str(ws.cell(i, 0).value).strip()

            estilo = wb.xf_list[ws.cell_xf_index(i, 0)]
            recuo = estilo.alignment.indent_level

            if recuo == 0:
                estado_atual = nome

            elif recuo == 3:
                dados.append([
                    ano,
                    estado_atual,
                    nome,
                    cultura,
                    ws.cell(i, 1).value,
                    ws.cell(i, 2).value,
                    ws.cell(i, 3).value,
                    ws.cell(i, 4).value,
                    ws.cell(i, 5).value
                ])

        df = pd.DataFrame(dados, columns=[
            "Ano",
            "Estado",
            "Municipio",
            "Cultura",
            "Area_Plantada",
            "Area_Colhida",
            "Producao_Ton",
            "Rendimento",
            "Valor"
        ])

        df["Estado_limpo"] = df["Estado"].apply(limpar_texto)
        df["UF"] = df["Estado_limpo"].map(estado_para_uf)

        # corrige os nomes dos municipio

        df["Municipio"] = df.apply(
            lambda linha: correcoes.get(
                (linha["Municipio"], linha["UF"]),
                linha["Municipio"]
            ),
            axis=1
        )

        df["Municipio_limpo"] = df["Municipio"].apply(limpar_texto)

        df = df.merge(
            municipios_ibge[["COD_IBGE", "Municipio_limpo", "UF"]],
            on=["Municipio_limpo", "UF"],
            how="left"
        )

        df = df.drop(columns=["Estado_limpo", "Municipio_limpo"])

        sem_codigo = df["COD_IBGE"].isna().sum()

        if sem_codigo > 0:
            df[df["COD_IBGE"].isna()].to_csv(
                os.path.join(pasta_saida, f"{cultura.lower()}_{ano}_sem_codigo.csv"),
                index=False,
                encoding="utf-8-sig"
            )

        saida = os.path.join(pasta_saida, f"{cultura.lower()}_{ano}.csv")
        df.to_csv(saida, index=False, encoding="utf-8-sig")


for ano in range(2009, 2017):
    print(f"Tratando {ano}...")
    tratamento(ano)