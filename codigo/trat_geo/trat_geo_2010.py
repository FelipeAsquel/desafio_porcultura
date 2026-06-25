from dbfread import DBF
import pandas as pd
import os

pasta = r"C:\Users\pc\OneDrive\Área de Trabalho\desafio_final\da_geo\2010"
saida_csv = r"da_geo\2010\municipios_ibge_2010.csv"

codigo_uf = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA",
    "16": "AP", "17": "TO", "21": "MA", "22": "PI", "23": "CE",
    "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE",
    "29": "BA", "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
    "41": "PR", "42": "SC", "43": "RS", "50": "MS", "51": "MT",
    "52": "GO", "53": "DF"
}

tabelas = []

for raiz, pastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        if arquivo.lower().endswith(".dbf"):
            caminho_dbf = os.path.join(raiz, arquivo)

            tabela = DBF(
                caminho_dbf,
                encoding="latin1",
                char_decode_errors="ignore"
            )

            df = pd.DataFrame(iter(tabela))

            tabela = DBF(
    caminho_dbf,
    encoding="latin1",
    char_decode_errors="ignore"
)

            municipios = df[["CD_GEOCODM", "NM_MUNICIP"]].copy()
            municipios.columns = ["COD_IBGE", "MUNICIPIO"]

            municipios["COD_IBGE"] = municipios["COD_IBGE"].astype(str)
            municipios["UF"] = municipios["COD_IBGE"].str[:2].map(codigo_uf)

            tabelas.append(municipios)

municipios_2010 = pd.concat(tabelas, ignore_index=True)

municipios_2010.to_csv(
    saida_csv,
    index=False,
    encoding="utf-8-sig"
)

print(saida_csv)
print("Total de municípios:", len(municipios_2010))
print(municipios_2010.head(20))