import geopandas as gpd
import pandas as pd


def validar_dataframe(df: pd.DataFrame) -> bool:
    """
    Valida um DataFrame para garantir que contenha as colunas necessárias com os tipos de dados corretos.

    Esta função verifica se o DataFrame fornecido contém todas as colunas definidas em
    REQUIRED_COLUMNS e se cada coluna possui o tipo de dado esperado. A validação é
    importante para garantir a integridade dos dados antes do processamento.

    Args:
        df (pd.DataFrame): DataFrame a ser validado. Deve conter as colunas:
            - Name (str): Nome do local
            - Latitude (float): Coordenada de latitude
            - Longitude (float): Coordenada de longitude

    Returns:
        bool: True se o DataFrame passar em todas as validações.

    Raises:
        ValueError: Se alguma coluna estiver faltando no DataFrame ou se alguma
            coluna tiver um tipo de dado incorreto. A mensagem de erro especificará
            qual validação falhou.

    Examples:
        >>> data = pd.DataFrame({
        ...     'Name': ['Local A', 'Local B'],
        ...     'Latitude': [-23.550520, -23.550520],
        ...     'Longitude': [-46.633308, -46.633308]
        ... })
        >>> validar_dataframe(data)
        True

        >>> # Isso irá gerar um ValueError
        >>> invalid_data = pd.DataFrame({
        ...     'Name': ['Local A'],
        ...     'Longitude': [-46.633308]
        ... })
        >>> validar_dataframe(invalid_data)
        ValueError: DataFrame está faltando colunas: ['Latitude']
    """

    REQUIRED_COLUMNS = {"Name": str, "Latitude": float, "Longitude": float}

    # Verifica se as colunas esperadas estão presentes
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"DataFrame está faltando colunas: {missing_columns}")

    # Verifica se os tipos das colunas estão corretos
    for col, col_type in REQUIRED_COLUMNS.items():
        if not pd.api.types.is_dtype_equal(
            df[col].dtype, pd.Series(dtype=col_type).dtype
        ):
            raise ValueError(f"Coluna '{col}' deve ser do tipo {col_type}")

    return True


def validar_gdf_city(df: pd.DataFrame) -> bool:
    required_columns = [
        "OBJECTID",
        "Shape_Leng",
        "Shape_Area",
        "Nome_Polo",
        "FID_1",
        "Shape_Ar_1",
        "Nome_Pol_1",
        "RendaDomc_",
        "Domicilios",
        "Moradores",
        "RendaPerca",
        "geometry",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"gdf_city está faltando colunas: {missing_columns}")
    return True


def validar_df_dados_linhas(df: pd.DataFrame) -> bool:
    required_columns = [
        "linha",
        "geometry",
        "via_pavimentada",
        "integracao",
        "treinamento_motorista",
        "informacao_internet",
        "valor_tarifa",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"df_dados_linhas está faltando colunas: {missing_columns}")
    return True


def validar_df_frequencia(df: pd.DataFrame) -> bool:
    required_columns = [
        "hsstart",
        "hsstop",
        "data",
        "sentido",
        "linha",
        "qtpsg",
        "valor_jornada",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"df_frequencia está faltando colunas: {missing_columns}")
    return True


def validar_df_pontualidade(df: pd.DataFrame) -> bool:
    required_columns = [
        "Data",
        "Trajeto",
        "Chegada ao ponto",
        "Partida Real",
        "Chegada Real",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"df_pontualidade está faltando colunas: {missing_columns}")
    return True


def validar_df_cumprimento(df: pd.DataFrame) -> bool:
    required_columns = [
        "Data",
        "Trajeto",
        "KM Executado",
    ]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"df_pontualidade está faltando colunas: {missing_columns}")
    return True


def validar_residencias(gdf: gpd.GeoDataFrame) -> bool:
    required_columns = ["ID", "Longitude", "Latitude"]
    missing_columns = [col for col in required_columns if col not in gdf.columns]
    if missing_columns:
        raise ValueError(f"gdf_residências está faltando colunas: {missing_columns}")
    return True


def validar_pontos_onibus(gdf: gpd.GeoDataFrame) -> bool:
    required_columns = ["ID", "Longitude", "Latitude"]
    missing_columns = [col for col in required_columns if col not in gdf.columns]
    if missing_columns:
        raise ValueError(f"gdf_pontos_onibus está faltando colunas: {missing_columns}")
    return True
