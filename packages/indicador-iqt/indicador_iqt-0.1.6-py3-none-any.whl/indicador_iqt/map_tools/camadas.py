import fiona
import folium
import folium.plugins
import geopandas as gpd
import pandas as pd
from shapely import wkt
from shapely.geometry import LineString

from ..utils.cores import cor_iqt, cor_aleatoria


def carregar_camadas_linhas(path_lines: str) -> gpd.GeoDataFrame:
    """
    Carrega camadas de linhas de um arquivo KML, excluindo a camada 'Linhas prontas'.

    Parameters
    ----------
    path_lines : str
        Caminho para o arquivo KML contendo as camadas de linhas.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame contendo todas as camadas de linhas concatenadas,
        exceto a camada 'Linhas prontas'.

    Notes
    -----
    Utiliza o driver LIBKML para leitura do arquivo e concatena todas as
    camadas válidas em um único GeoDataFrame.
    """
    gdf_list = []
    for layer in fiona.listlayers(path_lines):
        if layer == "Linhas prontas":
            continue
        gdf = gpd.read_file(path_lines, driver="LIBKML", layer=layer)
        gdf_list.append(gdf)
    gdf_lines = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))
    return gdf_lines


def filtrar_linhas(gdf: gpd.GeoDataFrame) -> pd.DataFrame | pd.Series:
    """
    Filtra o GeoDataFrame para manter apenas geometrias do tipo LineString.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame contendo diferentes tipos de geometrias.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame filtrado contendo apenas geometrias do tipo LineString.
    """
    return gdf[gdf.geometry.type == "LineString"]


def calcular_distancias(gdf_lines: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Calcula o comprimento de cada LineString no GeoDataFrame.

    Parameters
    ----------
    gdf_lines : gpd.GeoDataFrame
        GeoDataFrame contendo geometrias do tipo LineString.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame original com uma nova coluna 'distances' contendo
        o comprimento de cada linha.

    Notes
    -----
    O cálculo é feito utilizando o sistema de coordenadas atual do GeoDataFrame.
    Para resultados em metros, certifique-se que o CRS está em uma projeção adequada.
    """
    gdf_lines["distances"] = gdf_lines.apply(lambda row: row.geometry.length, axis=1)
    return gdf_lines


def calcular_distancias_2(gdf_lines: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Calcula distâncias em metros e quilômetros usando projeção Web Mercator (EPSG:3857).

    Parameters
    ----------
    gdf_lines : gpd.GeoDataFrame
        GeoDataFrame contendo geometrias do tipo LineString.

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame com novas colunas:
        - 'distancia_metros': comprimento da linha em metros
        - 'distancia_km': comprimento da linha em quilômetros
        O GeoDataFrame é retornado na projeção WGS84 (EPSG:4326).

    Notes
    -----
    A função realiza os seguintes passos:
    1. Reprojecta para Web Mercator (EPSG:3857)
    2. Calcula as distâncias
    3. Retorna o GeoDataFrame na projeção WGS84
    """
    gdf_lines = gdf_lines.to_crs(3857)
    gdf_lines["distancia_metros"] = gdf_lines.length
    gdf_lines["distancia_km"] = gdf_lines["distancia_metros"] / 1000
    return gdf_lines.to_crs(4326)


def criar_popup(line: pd.Series):
    popup_content = """
    <div style="max-width:300px;">
        <h4 style="margin-bottom:10px;">{}</h4>
        <table style="width:100%; border-collapse:collapse;">
    """.format(line.linha)

    # Adicionando todas as informações disponíveis na Series
    for idx, value in line.items():
        if idx != "geometry":  # Excluindo a coluna de geometria
            value = round(value, 2) if isinstance(value, float) else value
            popup_content += f"""
            <tr style="border-bottom:1px solid #ddd;">
                <td style="padding:5px;"><strong>{idx}</strong></td>
                <td style="padding:5px;">{value}</td>
            </tr>
            """
    popup_content += """
        </table>
    </div>
    """

    return popup_content


def adicionar_linha_ao_mapa(line: pd.Series, group: folium.FeatureGroup, color: str = "") -> None:
    """
    Adiciona uma linha ao mapa Folium com grupo específico.

    Parameters
    ----------
    line : gpd.GeoSeries
        Série do GeoPandas contendo a geometria da linha e seus atributos.
        Deve conter as seguintes colunas:
        - 'geometry': geometria do tipo LineString
        - 'Name': nome da linha para o tooltip
        - 'iqt': índice de qualidade para determinar a cor

    map_routes : folium.Map
        Objeto do mapa Folium onde a linha será adicionada.

    group : folium.FeatureGroup
        Grupo de features do Folium onde a linha será agrupada.

    Notes
    -----
    A cor da linha é determinada pela função cor_iqt com base no valor do IQT.
    """
    # geometry = wkt.loads(line.geometry)
    # tooltip_line = line['linha']
    color = color if color else cor_aleatoria()
    folium.PolyLine(
        locations=[(lat, lon) for lon, lat, *rest in line.geometry.coords],
        color=color,
        weight=2.5,
        opacity=1,
        tooltip=line.linha,
        popup=criar_popup(line),
    ).add_to(group)


def adicionar_linha_ao_mapa_sem_grupo(line: pd.Series, map_routes: folium.Map) -> None:
    """
    Adiciona uma linha diretamente ao mapa Folium sem agrupamento.

    Parameters
    ----------
    line : gpd.GeoSeries
        Série do GeoPandas contendo a geometria da linha e seus atributos.
        Deve conter as seguintes colunas:
        - 'geometry': geometria do tipo LineString
        - 'linha': nome da linha para o tooltip
        - 'iqt': índice de qualidade para determinar a cor

    map_routes : folium.Map
        Objeto do mapa Folium onde a linha será adicionada.

    Notes
    -----
    Similar a adicionar_linha_ao_mapa, mas adiciona a linha diretamente ao mapa
    sem usar grupos. A linha terá uma espessura maior (weight=3).
    """
    # Extraindo a geometria, tooltip e cor
    geometry = wkt.loads(line.geometry)
    # tooltip_line = line['linha']
    color = cor_iqt(line.iqt)

    # Verificando se a geometria é um LineString
    if isinstance(geometry, LineString):
        # Extraindo as coordenadas para o PolyLine
        locations = [(lat, lon) for lon, lat, *rest in geometry.coords]
        # Adicionando a linha ao mapa com Folium
        folium.PolyLine(
            locations=locations, color=color, weight=3, opacity=1, tooltip=line.linha
        ).add_to(map_routes)
    else:
        raise TypeError("A geometria fornecida não é do tipo LineString.")


def coordenadas_pontos_linhas(line: gpd.GeoSeries) -> list[tuple[float, float]]:
    # geometry = wkt.loads(line.geometry)
    return [(lat, lon) for lon, lat, *rest in line.coords]
