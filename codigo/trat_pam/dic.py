import unicodedata
import pandas as pd
import os

def limpar_texto(txt):
    if pd.isna(txt):
        return ""

    txt = str(txt).strip().upper()
    txt = unicodedata.normalize("NFKD", txt)
    txt = "".join(c for c in txt if not unicodedata.combining(c))
    return txt

def ano_municipio(ano):
    if ano == 2009:
        return 2010
    elif ano == 2010 or ano == 2011 or ano == 2012 or ano == 2013 or ano == 2014 or ano == 2015:
        return 2015
    else:
        return 2016
    
CORRECOES = {
    "2009": {
    ("Eldorado do Carajás", "PA"): "Eldorado dos Carajás",
    ("Couto de Magalhães", "TO"): "Couto Magalhães",
    ("São Valério da Natividade", "TO"): "São Valério",
    ("Itapajé", "CE"): "Itapagé",
    ("Serra Caiada", "RN"): "Presidente Juscelino",
    ("São Domingos de Pombal", "PB"): "São Domingos",
    ("São Vicente do Seridó", "PB"): "Seridó",
    ("Campo de Santana", "PB"): "Tacima",
    ("Iguaracy", "PE"): "Iguaraci",
    ("Belém de São Francisco", "PE"): "Belém do São Francisco",
    ("Lagoa do Itaenga", "PE"): "Lagoa de Itaenga",
    ("Brazópolis", "MG"): "Brasópolis",
    ("Trajano de Morais", "RJ"): "Trajano de Moraes",
    ("Mogi Mirim", "SP"): "Moji Mirim",
    ("Santana do Livramento", "RS"): "Sant'Ana do Livramento",
    ("Poxoréu", "MT"): "Poxoréo",
    },
    "2010": {
    ("Eldorado dos Carajás", "PA"): "Eldorado do Carajás",
    ("Itapagé", "CE"): "Itapajé",
    ("Iguaraci", "PE"): "Iguaracy",
    ("Poxoréo", "MT"): "Poxoréu",
    ("Moji Mirim", "SP"): "Mogi Mirim",
    ("Brasópolis", "MG"): "Brazópolis",
    ("Presidente Juscelino", "RN"): "Serra Caiada",
    ("Seridó", "PB"): "São Vicente do Seridó",
    },
    "2011":{  
    ("Eldorado dos Carajás", "PA"): "Eldorado do Carajás",
    ("Itapagé", "CE"): "Itapajé",
    ("Iguaraci", "PE"): "Iguaracy",
    ("Poxoréo", "MT"): "Poxoréu",
    ("Moji Mirim", "SP"): "Mogi Mirim",
    ("Brasópolis", "MG"): "Brazópolis",
    ("Presidente Juscelino", "RN"): "Serra Caiada",
    ("Seridó", "PB"): "São Vicente do Seridó",
    },
    "2012": {
    ("Eldorado dos Carajás", "PA"): "Eldorado do Carajás",
    ("Itapagé", "CE"): "Itapajé",
    ("Iguaraci", "PE"): "Iguaracy",
    ("Poxoréo", "MT"): "Poxoréu",
    ("Moji Mirim", "SP"): "Mogi Mirim",
    ("Brasópolis", "MG"): "Brazópolis",
    ("Presidente Juscelino", "RN"): "Serra Caiada",
    ("Seridó", "PB"): "São Vicente do Seridó",
    },
    "2013":{
    ("Eldorado dos Carajás", "PA"): "Eldorado do Carajás",
    ("Itapagé", "CE"): "Itapajé",
    ("Iguaraci", "PE"): "Iguaracy",
    ("Poxoréo", "MT"): "Poxoréu",
    ("Moji Mirim", "SP"): "Mogi Mirim",
    ("Brasópolis", "MG"): "Brazópolis",
    ("Presidente Juscelino", "RN"): "Serra Caiada",
    ("Seridó", "PB"): "São Vicente do Seridó",
    },
    "2014":{
    ("Eldorado dos Carajás", "PA"): "Eldorado do Carajás",
    ("Itapagé", "CE"): "Itapajé",
    ("Iguaraci", "PE"): "Iguaracy",
    ("Poxoréo", "MT"): "Poxoréu",
    ("Moji Mirim", "SP"): "Mogi Mirim",
    ("Brasópolis", "MG"): "Brazópolis",
    ("Presidente Juscelino", "RN"): "Serra Caiada",
    ("Seridó", "PB"): "São Vicente do Seridó",
    },
    "2015":{
    ("Eldorado dos Carajás", "PA"): "Eldorado do Carajás",
    ("Itapagé", "CE"): "Itapajé",
    ("Iguaraci", "PE"): "Iguaracy",
    ("Poxoréo", "MT"): "Poxoréu",
    ("Moji Mirim", "SP"): "Mogi Mirim",
    ("Brasópolis", "MG"): "Brazópolis",
    ("Presidente Juscelino", "RN"): "Serra Caiada",
    ("Seridó", "PB"): "São Vicente do Seridó",
    },
    "2016":{
    ("Eldorado dos Carajás", "PA"): "Eldorado do Carajás",
    ("Itapagé", "CE"): "Itapajé",
    ("Iguaraci", "PE"): "Iguaracy",
    ("Pingo-d'Água", "MG"): "Pingo D'Água",
    ("Passa-Vinte", "MG"): "Passa Vinte",
    ("Biritiba-Mirim", "SP"): "Biritiba Mirim",
    ("Poxoréo", "MT"): "Poxoréu",
    ("Moji Mirim", "SP"): "Mogi Mirim",
    ("Florínia", "SP"): "Florínea",
    ("Muquém de São Francisco", "BA"): "Muquém do São Francisco",
    ("Olho-d'Água do Borges", "RN"): "Olho D'Água do Borges",
    ("Brasópolis", "MG"): "Brazópolis",
    ("São Luís do Paraitinga", "SP"): "São Luiz do Paraitinga",
    ("Santa Teresinha", "BA"): "Santa Terezinha",
    ("Presidente Juscelino", "RN"): "Serra Caiada",
    ("Seridó", "PB"): "São Vicente do Seridó",
    }
}

estado_para_uf = {
    "RONDONIA": "RO", "ACRE": "AC", "AMAZONAS": "AM", "RORAIMA": "RR",
    "PARA": "PA", "AMAPA": "AP", "TOCANTINS": "TO", "MARANHAO": "MA",
    "PIAUI": "PI", "CEARA": "CE", "RIO GRANDE DO NORTE": "RN",
    "PARAIBA": "PB", "PERNAMBUCO": "PE", "ALAGOAS": "AL",
    "SERGIPE": "SE", "BAHIA": "BA", "MINAS GERAIS": "MG",
    "ESPIRITO SANTO": "ES", "RIO DE JANEIRO": "RJ", "SAO PAULO": "SP",
    "PARANA": "PR", "SANTA CATARINA": "SC", "RIO GRANDE DO SUL": "RS",
    "MATO GROSSO DO SUL": "MS", "MATO GROSSO": "MT", "GOIAS": "GO",
    "DISTRITO FEDERAL": "DF"
}