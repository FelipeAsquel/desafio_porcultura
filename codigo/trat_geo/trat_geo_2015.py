from dbfread import DBF
import pandas as pd

arquivo_dbf = r"C:\Users\pc\OneDrive\Área de Trabalho\desafio_final\da_geo\2015\malha2015.dbf"
saida_csv = r"da_geo\2015\municipios_ibge_2015.csv"

tabela = DBF(
    arquivo_dbf,
    encoding="latin1",
    char_decode_errors="ignore"
)

df = pd.DataFrame(iter(tabela))

for coluna in df.select_dtypes(include="object").columns:
    df[coluna] = df[coluna].apply(
        lambda x: x.encode("latin1").decode("utf-8", errors="ignore")
        if isinstance(x, str)
        else x
    )

municipios = df[["CD_GEOCMU", "NM_MUNICIP"]].copy()

municipios.columns = ["COD_IBGE", "MUNICIPIO"]

municipios["COD_IBGE"] = municipios["COD_IBGE"].astype(str)

codigo_uf = {
    "11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA",
    "16": "AP", "17": "TO", "21": "MA", "22": "PI", "23": "CE",
    "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE",
    "29": "BA", "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
    "41": "PR", "42": "SC", "43": "RS", "50": "MS", "51": "MT",
    "52": "GO", "53": "DF"
}

municipios["UF"] = municipios["COD_IBGE"].str[:2].map(codigo_uf)

municipios.to_csv(
    saida_csv,
    index=False,
    encoding="utf-8-sig"
)

print(saida_csv)
print(municipios.head(10))