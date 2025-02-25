import pandas as pd


def viagens_por_rota(df: pd.DataFrame) -> pd.Series:
    """Calcula o número de viagens realizadas por rota (linha).

    Args:
        df (pd.DataFrame): DataFrame contendo dados das viagens com a coluna 'linha' para identificar a rota e 'empresa' para as contagens.

    Returns:
        pd.DataFrame: DataFrame com a contagem de viagens por rota.

    Example:
        >>> viagens_por_rota(df)
        linha
        101      50
        102      30
        103      20
    """
    return df.groupby("linha")["empresa"].count()


def media_passageiros_por_rota(df: pd.DataFrame) -> pd.Series:
    """Calcula a média de passageiros por rota (linha).

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar a rota e 'qtpsg' para quantidade de passageiros.

    Returns:
        pd.DataFrame: DataFrame com a média de passageiros por rota.

    Example:
        >>> media_passageiros_por_rota(df)
        linha
        101      25.0
        102      30.5
        103      22.3
    """
    return df.groupby("linha")["qtpsg"].mean()


def valor_arrecadado_por_rota(df: pd.DataFrame) -> pd.Series:
    """Calcula o valor total arrecadado por rota (linha).

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar a rota e 'valor_jornada' para os valores arrecadados.

    Returns:
        pd.DataFrame: DataFrame com o valor arrecadado por rota.

    Example:
        >>> valor_arrecadado_por_rota(df)
        linha
        101     10000.0
        102      8500.5
        103      9200.2
    """
    return df.groupby("linha")["valor_jornada"].sum()


def tempo_medio_operacao(df: pd.DataFrame) -> pd.Series:
    """Calcula o tempo médio de operação por rota (linha).

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar a rota e 'duracao' para a duração das viagens.

    Returns:
        pd.DataFrame: DataFrame com o tempo médio de operação por rota.

    Example:
        >>> tempo_medio_operacao(df)
        linha
        101     45.0
        102     37.5
        103     50.2
    """
    return df.groupby("linha")["duracao"].mean()


def demanda_comparativa(df: pd.DataFrame) -> pd.Series:
    """Calcula a demanda total de passageiros por rota, em ordem decrescente.

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar a rota e 'qtpsg' para a quantidade de passageiros.

    Returns:
        pd.DataFrame: DataFrame com a demanda total de passageiros por rota, ordenado de forma decrescente.

    Example:
        >>> demanda_comparativa(df)
        linha
        103     3000
        101     2500
        102     2000
    """
    return df.groupby("linha")["qtpsg"].sum().sort_values(ascending=False)


def comparacao_valores(df: pd.DataFrame) -> pd.Series:
    """Compara o valor arrecadado por rota em ordem decrescente.

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar a rota e 'valor_jornada' para os valores arrecadados.

    Returns:
        pd.DataFrame: DataFrame com o valor arrecadado por rota, ordenado de forma decrescente.

    Example:
        >>> comparacao_valores(df)
        linha
        103     15000.0
        101     12000.5
        102      9500.0
    """
    return df.groupby("linha")["valor_jornada"].sum().sort_values(ascending=False)


def agrupar_por_dia(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa dados de passageiros e valor arrecadado por dia e por rota.

    Args:
        df (pd.DataFrame): DataFrame contendo as colunas 'data' para data, 'linha' para rota,
            'qtpsg' para quantidade de passageiros e 'valor_jornada' para valor arrecadado.

    Returns:
        pd.DataFrame: DataFrame com o total de passageiros e valor arrecadado agrupado por dia e por rota.

    Example:
        >>> agrupar_por_dia(df)
            data    linha   qtpsg  valor_jornada
        0  2023-01-01  101     100      1500.0
        1  2023-01-02  102      80      1200.0
    """
    return df.groupby(["data", "linha"])[["qtpsg", "valor_jornada"]].sum().reset_index()


def agrupar_duracao_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa a duração média das viagens por mês e por rota.

    Args:
        df (pd.DataFrame): DataFrame contendo a coluna 'data' para data e 'linha' para rota,
            e 'duracao_minutos' para duração das viagens em minutos.

    Returns:
        pd.DataFrame: DataFrame com a duração média das viagens por mês e rota.

    Example:
        >>> agrupar_duracao_por_mes(df)
           mes  linha   duracao_minutos
        0   1     101      40.5
        1   1     102      30.0
        2   2     103      45.2
    """
    df["mes"] = df["data"].dt.month
    return df.groupby(["mes", "linha"])["duracao_minutos"].mean().reset_index()
