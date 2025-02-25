# coef_analysis/correlation.py

import pandas as pd
import numpy as np

def get_coef(data, alvo, limite=[-0.01, 0.01], ascending = False):
    """
    Calcula o coeficiente de correlação entre as colunas de um DataFrame e uma variável alvo.

    Parâmetros:
    -----------
    data : pandas.DataFrame
        O DataFrame contendo os dados.
    alvo : str
        O nome da variável alvo para calcular a correlação.
    limite : list, opcional
        Lista com dois valores que definem o limite de correlação considerada significativa.

    Retorna:
    --------
    pandas.DataFrame
        DataFrame com as colunas que possuem correlação fora dos limites estabelecidos.

    Levanta:
    --------
    ValueError
        Se nenhuma coluna satisfizer os critérios de correlação.
    """
    if alvo not in data.columns:
        raise ValueError(f"A variável alvo '{alvo}' não está presente no DataFrame.")

    corr_dict = {}
    for i in data.columns:
        if i == alvo:
            continue
        coef = np.corrcoef(data[i], data[alvo])[0, 1]
        if coef <= limite[0] or coef >= limite[1]:
            corr_dict.update({i: round(coef, 3)})

    if len(corr_dict) == 0:
        raise ValueError("Ajuste seu Limite: Nenhuma correlação encontrada dentro dos critérios.")
    else:
        dataframe_corr = pd.DataFrame(list(corr_dict.items()), columns = ['Valores', 'Coeficiente de Correlação'])

    if ascending == False:
        dataframe_corr = dataframe_corr.sort_values('Coeficiente de Correlação', ignore_index = True, ascending = False)
    else:
        dataframe_corr = dataframe_corr.sort_values('Coeficiente de Correlação', ignore_index = True, ascending = True)


    return dataframe_corr
