import geopandas as gpd
import pandas as pd
import pytest
from shapely.geometry import Point

from indicador_iqt.utils.modelos import (
    validar_dataframe,
    validar_df_cumprimento,
    validar_df_dados_linhas,
    validar_df_frequencia,
    validar_df_pontualidade,
    validar_gdf_city,
    validar_pontos_onibus,
    validar_residencias,
)


def test_validar_dataframe_success():
    """Test successful DataFrame validation."""
    df = pd.DataFrame(
        {
            "Name": ["Local A", "Local B"],
            "Latitude": [-23.550520, -23.550520],
            "Longitude": [-46.633308, -46.633308],
        }
    )
    assert validar_dataframe(df)


def test_validar_dataframe_missing_columns():
    """Test validation with missing columns."""
    df = pd.DataFrame({"Name": ["Local A"], "Longitude": [-46.633308]})
    with pytest.raises(ValueError):
        validar_dataframe(df)


def test_validar_dataframe_incorrect_types():
    """Test validation with incorrect column types."""
    df = pd.DataFrame(
        {
            "Name": ["Local A", "Local B"],
            "Latitude": ["23.550520", "23.550520"],  # string instead of float
            "Longitude": [-46.633308, -46.633308],
        }
    )
    with pytest.raises(ValueError, match="Coluna 'Latitude' deve ser do tipo"):
        validar_dataframe(df)


def test_validar_gdf_city():
    """Test GeoDataFrame city validation."""
    gdf = gpd.GeoDataFrame(
        {
            "OBJECTID": [1, 2],
            "Shape_Leng": [100.0, 200.0],
            "Shape_Area": [1000.0, 2000.0],
            "Nome_Polo": ["Polo1", "Polo2"],
            "FID_1": [1, 2],
            "Shape_Ar_1": [1000.0, 2000.0],
            "Nome_Pol_1": ["Pol1", "Pol2"],
            "RendaDomc_": [1000, 2000],
            "Domicilios": [100, 200],
            "Moradores": [250, 500],
            "RendaPerca": [50.0, 100.0],
            "geometry": [Point(0, 0), Point(1, 1)],
        }
    )
    assert validar_gdf_city(gdf)


def test_validar_gdf_city_missing_columns():
    """Test GeoDataFrame city validation with missing columns."""
    gdf = gpd.GeoDataFrame({"OBJECTID": [1, 2], "Shape_Leng": [100.0, 200.0]})
    with pytest.raises(ValueError, match="gdf_city está faltando colunas"):
        validar_gdf_city(gdf)


def test_validar_df_dados_linhas():
    """Test dados linhas DataFrame validation."""
    df = pd.DataFrame(
        {
            "linha": ["L1", "L2"],
            "geometry": ["LINESTRING(0 0, 1 1)", "LINESTRING(1 1, 2 2)"],
            "via_pavimentada": [1, 0],
            "integracao": ["Integrado", "Parcial"],
            "treinamento_motorista": [1.0, 0.5],
            "informacao_internet": ["Site", "App"],
            "valor_tarifa": ["Atual", "Antigo"],
        }
    )
    assert validar_df_dados_linhas(df)


def test_validar_df_frequencia():
    """Test frequência DataFrame validation."""
    df = pd.DataFrame(
        {
            "hsstart": ["06:00:00", "07:00:00"],
            "hsstop": ["07:00:00", "08:00:00"],
            "data": ["01/01/2024", "02/01/2024"],
            "sentido": [0, 1],
            "linha": ["L1", "L2"],
            "qtpsg": [10, 20],
            "valor_jornada": [100, 200],
        }
    )
    assert validar_df_frequencia(df)


def test_validar_df_pontualidade():
    """Test pontualidade DataFrame validation."""
    df = pd.DataFrame(
        {
            "Data": ["01/01/2024", "02/01/2024"],
            "Trajeto": ["Rota1", "Rota2"],
            "Chegada ao ponto": ["06:00:00", "07:00:00"],
            "Partida Real": ["06:05:00", "07:05:00"],
            "Chegada Real": ["06:55:00", "07:55:00"],
        }
    )
    assert validar_df_pontualidade(df)


def test_validar_df_cumprimento():
    """Test cumprimento DataFrame validation."""
    df = pd.DataFrame(
        {
            "Data": ["01/01/2024", "02/01/2024"],
            "Trajeto": ["Rota1", "Rota2"],
            "KM Executado": [10.5, 20.5],
        }
    )
    assert validar_df_cumprimento(df)


def test_validar_residencias():
    """Test residências GeoDataFrame validation."""
    gdf = gpd.GeoDataFrame(
        {
            "ID": [1, 2],
            "Longitude": [-46.633308, -46.633309],
            "Latitude": [-23.550520, -23.550521],
            "geometry": [Point(-46.633308, -23.550520), Point(-46.633309, -23.550521)],
        }
    )
    assert validar_residencias(gdf)


def test_validar_pontos_onibus():
    """Test pontos ônibus GeoDataFrame validation."""
    gdf = gpd.GeoDataFrame(
        {
            "ID": [1, 2],
            "Longitude": [-46.633308, -46.633309],
            "Latitude": [-23.550520, -23.550521],
            "geometry": [Point(-46.633308, -23.550520), Point(-46.633309, -23.550521)],
        }
    )
    assert validar_pontos_onibus(gdf)
