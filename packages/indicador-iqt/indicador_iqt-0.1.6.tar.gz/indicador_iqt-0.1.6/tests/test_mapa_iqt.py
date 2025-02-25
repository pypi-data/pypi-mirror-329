import pytest
from shapely.geometry import Polygon
import geopandas as gpd
from indicador_iqt.map_tools import MapaIQT
import folium

@pytest.fixture
def dados_mapa():
    dados = {
        'Nome_Polo': ["Maracanã"],
    }
    # coordenadas = ((-43.84614005469888, -16.750643375323758),(-43.84614005469888,-16.750624339635692),(-43.845868808488945,-16.750791298594944), (-43.84535912270718,-16.750956922802004),(-43.84486732094962,-16.75119542524391),(-43.842556716816546,-16.751722334665942))
    # geometry = [Polygon(coordenadas)]
    geometrias = [Polygon([(-43.84614005469888, -16.750643375323758),(-43.84614005469888,-16.750624339635692),(-43.845868808488945,-16.750791298594944), (-43.84535912270718,-16.750956922802004),(-43.84486732094962,-16.75119542524391),(-43.842556716816546,-16.751722334665942)])]
    
    gdf = gpd.GeoDataFrame(dados, geometry=geometrias)
    
    # Define o CRS (use "EPSG:4326" ou o CRS correto para seus dados)
    gdf.set_crs("EPSG:4326", allow_override=True, inplace=True)
    
    return gdf

def test_iniciar_mapa(dados_mapa):
    mapa = MapaIQT(dados_mapa)
    assert isinstance(mapa.map, folium.Map)