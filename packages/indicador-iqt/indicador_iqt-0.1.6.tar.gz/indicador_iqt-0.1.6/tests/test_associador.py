import pytest
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import LineString
from indicador_iqt.utils.associador import Associador

@pytest.fixture
def sample_residencias():
    """Fixture que cria um DataFrame de residências para teste."""
    return pd.DataFrame({
        'Longitude': [-43.9386, -43.9389, -43.9392],
        'Latitude': [-19.9176, -19.9179, -19.9182],
        'ID': [1, 2, 3]
    })

@pytest.fixture
def sample_pontos_onibus():
    """Fixture que cria um DataFrame de pontos de ônibus para teste."""
    return pd.DataFrame({
        'Longitude': [-43.9387, -43.9390],
        'Latitude': [-19.9177, -19.9180],
        'ID': [1, 2]
    })

@pytest.fixture
def sample_linhas():
    """Fixture que cria um GeoDataFrame de linhas de ônibus para teste."""
    geometries = [
        LineString([[-43.9387, -19.9177], [-43.9387, -19.9177], [-43.9387, -19.9179]]),
        LineString([[-43.9353, -19.9177], [-43.9381, -19.9174], [-43.9379, -19.9181]])
    ]
    return gpd.GeoDataFrame(data = {
        'linha': ['L001', 'L002'],
        # 'coordenadas_linhas' : geometries:
        'geometry': geometries
    }, crs="EPSG:4326")

@pytest.fixture
def associador(sample_residencias, sample_pontos_onibus, sample_linhas):
    """Fixture que cria uma instância da classe Associador com dados de teste."""
    return Associador(sample_pontos_onibus, sample_linhas, sample_residencias)

def test_init(associador):
    """Testa se a inicialização da classe está correta."""
    assert isinstance(associador.gdf_residencias, gpd.GeoDataFrame)
    assert isinstance(associador.gdf_pontos_onibus, gpd.GeoDataFrame)
    assert isinstance(associador.linhas, gpd.GeoDataFrame)
    assert associador.gdf_residencias.crs == "EPSG:32723"
    assert associador.gdf_pontos_onibus.crs == "EPSG:32723"

def test_verificar_formato_coordenadas(associador, sample_residencias):
    """Testa a verificação do formato das coordenadas."""
    assert associador._verificar_formato_coordenadas(sample_residencias) is np.True_
    
    # Teste com coordenadas inválidas
    invalid_coords = pd.DataFrame({
        'Longitude': [200, -200],
        'Latitude': [100, -100]
    })
    assert associador._verificar_formato_coordenadas(invalid_coords) is np.False_

def test_extrair_coordenadas(associador):
    """Testa a extração de coordenadas."""
    coords_residencias, coords_pontos_onibus = associador._extrair_coordenadas()
    
    assert isinstance(coords_residencias, np.ndarray)
    assert isinstance(coords_pontos_onibus, np.ndarray)
    assert coords_residencias.shape[1] == 2  # x, y coordinates
    assert coords_pontos_onibus.shape[1] == 2

def test_euclidean_distance(associador):
    """Testa o cálculo da distância euclidiana."""
    coord1 = np.array([[0, 0]])
    coord2 = np.array([[3, 4]])
    distance = associador.euclidean_distance(coord1, coord2)
    assert np.isclose(distance[0], 5.0)  # 3-4-5 triangle

def test_associar_residencias_a_pontos(associador):
    """Testa a associação de residências a pontos de ônibus."""
    associacoes = associador.associar_residencias_a_pontos()
    
    assert isinstance(associacoes, pd.DataFrame)
    assert len(associacoes) == len(associador.coords_residencias)

def test_associar_pontos_a_linhas(associador):
    """Testa a associação de pontos de ônibus a linhas."""
    associacoes = associador.associar_ponto_a_linha()

    assert isinstance(associacoes, dict)
    assert len(associacoes) == len(associador.coords_pontos_onibus)

def test_consolidar_associacoes(associador):
    """Testa a consolidação final das associações."""
    consolidado = associador.consolidar_associacoes()
    
    assert not consolidado.empty