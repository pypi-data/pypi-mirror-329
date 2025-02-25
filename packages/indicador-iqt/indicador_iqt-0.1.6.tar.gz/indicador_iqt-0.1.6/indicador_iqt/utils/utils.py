import pandas as pd

def converter_para_datetime(df, coluna, formato):
    """Converte uma coluna para o formato datetime especificado."""
    df[coluna] = pd.to_datetime(df[coluna], format=formato)
    return df
