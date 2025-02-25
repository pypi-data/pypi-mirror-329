import fiona
import geopandas as gpd
import pandas as pd


def carregar_rotas(file_path: str) -> pd.DataFrame:
    """
    Carrega rotas de transporte público a partir de um arquivo KML.

    Parameters
    ----------
    file_path : str
        Caminho para o arquivo KML contendo as rotas de transporte.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame contendo as rotas processadas com as seguintes colunas:
        - geometry: geometria da rota
        - linha: número ou identificador da linha
        - sentido: direção ou sentido da linha
        - Description: descrição da rota (rotas sem descrição são filtradas)

    Notes
    -----
    A função realiza os seguintes passos:
    1. Habilita suporte ao driver KML
    2. Carrega todas as camadas do arquivo KML
    3. Concatena as camadas em um único GeoDataFrame
    4. Filtra rotas sem descrição
    5. Separa o campo 'Name' em 'linha' e 'sentido'

    Examples
    --------
    >>> gdf_routes = carregar_rotas('caminho/para/rotas.kml')
    >>> print(gdf_routes.columns)
    Index(['geometry', 'Description', 'linha', 'sentido'])

    Raises
    ------
    FileNotFoundError
        Se o arquivo especificado não existir
    fiona.errors.DriverError
        Se houver problema com o driver KML
    ValueError
        Se o arquivo não contiver as colunas esperadas
    """
    # Habilita suporte ao driver KML
    # fiona.supported_drivers["libkml"] = "rw"
    # fiona.supported_drivers["LIBKML"] = "rw"

    # Carrega todas as camadas
    gdf_list = []
    for layer in fiona.listlayers(file_path):
        gdf = gpd.read_file(file_path, driver="LIBKML", layer=layer)
        gdf_list.append(gdf)

    # Concatena e processa os dados
    gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
    gdf = gdf.query("Description != ''")
    gdf[["linha", "sentido"]] = gdf["Name"].str.split(" - ", expand=True) # type: ignore
    del gdf["Name"]

    return gdf


def carregar_bairros(file_path: str) -> gpd.GeoDataFrame:
    """
    Carrega os bairros da cidade a partir de um arquivo geoespacial.

    Parameters
    ----------
    file_path : str
        Caminho para o arquivo contendo os polígonos dos bairros.
        Suporta formatos compatíveis com GeoPandas (Shapefile, GeoJSON, etc.).

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame contendo os polígonos dos bairros.

    Notes
    -----
    O CRS (Sistema de Referência de Coordenadas) do arquivo é mantido.
    Há código comentado para reprojeção para Web Mercator (EPSG:3857)
    se necessário no futuro.

    Examples
    --------
    >>> gdf_neighborhoods = carregar_bairros('caminho/para/bairros.shp')
    >>> print(gdf_neighborhoods.crs)

    Raises
    ------
    FileNotFoundError
        Se o arquivo especificado não existir
    fiona.errors.DriverError
        Se o formato do arquivo não for suportado
    """
    gdf_city = gpd.read_file(file_path)
    # Código comentado para possível reprojeção futura
    # gdf_city = gdf_city.to_crs(epsg=3857)
    return gpd.GeoDataFrame(gdf_city)
