import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import LineString, Point
from typing import Optional


class Associador:
    
    EARTH_CRS = "EPSG:4326"  # WGS 84
    LOCAL_CRS = "EPSG:32723"  # UTM 23S para Minas Gerais
    MAX_DISTANCE = 1000  # metros - distância máxima aceitável
    REQUIRED_COLUMNS = {'Latitude', 'Longitude'}
    
    def __init__(self, pontos_onibus: pd.DataFrame, linhas: gpd.GeoDataFrame, residencias: pd.DataFrame):
        """
        Inicializa a classe com os dados necessários.

        Args:
            pontos_onibus (pd.DataFrame): DataFrame com coordenadas dos pontos de ônibus
            linhas (pd.DataFrame): DataFrame com as linhas de ônibus
            residencias (pd.DataFrame): DataFrame com coordenadas das residências
        """
        # Criar GeoDataFrames e arrays NumPy
        self.gdf_residencias, self.gdf_pontos_onibus = self._criar_geodataframes(residencias, pontos_onibus)
        self.gdf_residencias = self.gdf_residencias.to_crs(self.LOCAL_CRS)  # UTM 23S para Minas Gerais
        self.gdf_pontos_onibus = self.gdf_pontos_onibus.to_crs(self.LOCAL_CRS)
        self.linhas = linhas.to_crs(self.LOCAL_CRS)
        
        self.coords_residencias, self.coords_pontos_onibus = self._extrair_coordenadas()

    def _verificar_formato_coordenadas(self, df: pd.DataFrame) -> bool:
        """Verifica se as coordenadas estão no formato decimal padrão."""
        longitude_ok = (-180 <= df['Longitude'].max() <= 180) and (-180 <= df['Longitude'].min() <= 180)
        latitude_ok = (-90 <= df['Latitude'].max() <= 90) and (-90 <= df['Latitude'].min() <= 90)
        return longitude_ok and latitude_ok

    def _extrair_coordenadas(self) -> tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Extrai coordenadas dos GeoDataFrames e converte para arrays NumPy.
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: Arrays com coordenadas das residências e pontos de ônibus
        """
        # Extrair coordenadas das residências
        if isinstance(self.gdf_pontos_onibus, gpd.GeoDataFrame) and isinstance(self.gdf_residencias, gpd.GeoDataFrame):
            coords_residencias = np.array([
                [geom.x, geom.y] 
                for geom in self.gdf_residencias.geometry
            ])
            
            # Extrair coordenadas dos pontos de ônibus
            coords_pontos_onibus = np.array([
                [geom.x, geom.y] 
                for geom in self.gdf_pontos_onibus.geometry
            ])
            
            return coords_residencias, coords_pontos_onibus
        return None, None

    def _criar_geodataframes(self, df_residencias: pd.DataFrame, df_pontos_onibus: pd.DataFrame) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
        """Converte DataFrames para GeoDataFrames."""
        residencias = df_residencias.copy()
        
        # Normalização de coordenadas se necessário
        if not self._verificar_formato_coordenadas(residencias):
            print("Normalizando coordenadas das residências...")
            residencias['Longitude'] = residencias['Longitude'] / 1000000
            residencias['Latitude'] = residencias['Latitude'] / 1000000
        else:
            print("Coordenadas das residências já estão no formato correto.")
        
        if not self._verificar_formato_coordenadas(df_pontos_onibus):
            raise ValueError("Coordenadas dos pontos de ônibus estão em formato incorreto!")
        
        # Criar geometrias como GeoSeries
        geometry_residencias = gpd.GeoSeries([
            Point(xy) for xy in zip(residencias['Longitude'], residencias['Latitude'])
        ])
        
        geometry_onibus = gpd.GeoSeries([
            Point(xy) for xy in zip(df_pontos_onibus['Longitude'], df_pontos_onibus['Latitude'])
        ])
        
        # Criar GeoDataFrames
        gdf_residencias = gpd.GeoDataFrame( 
            data=residencias, 
            geometry=geometry_residencias,
            crs=self.EARTH_CRS
        ) # type: ignore
        
        gdf_pontos_onibus = gpd.GeoDataFrame( 
            data=df_pontos_onibus, 
            geometry=geometry_onibus,
            crs=self.EARTH_CRS
        ) # type: ignore
        
        return gdf_residencias, gdf_pontos_onibus

    def distancia_euclidiana(self, coord1: np.ndarray, coord2: np.ndarray, axis : int = 1) -> np.ndarray:
        """Calcula a distância euclidiana entre dois conjuntos de coordenadas."""
        return np.sqrt(np.sum(np.square(coord1 - coord2), axis=axis))
    
    def _linestring_to_array(self, linestring : LineString):
        """
        Converte uma Linestring em um array numpy com formato [[[x1,y1]], [[x2,y2]], ...]
        
        Parâmetros:
        linestring (LineString): Objeto Linestring do Shapely
        
        Retorna:
        numpy.ndarray: Array com formato [[[x1,y1]], [[x2,y2]], ...]
        """
        # Extrai as coordenadas da linestring
        coords = list(linestring.coords)
        
        # Converte para o formato desejado
        array = np.array([[[x, y]] for x, y in coords])
        
        return array

    
    def associar_ponto_a_linha(self):
        # {`01`: [1, 2, 3], '02': [4, 8, 10]}
        relacionamento = {}
        if self.linhas is None:
            raise
        for _, linha in self.linhas.iterrows():
            nome_linha : str = linha.linha
            geometria_linha = linha.geometry
            relacionamento[nome_linha] = set()
            pontos_compoe_linhas_onibus = self._linestring_to_array(geometria_linha)
            distancia = self.distancia_euclidiana(pontos_compoe_linhas_onibus, self.coords_pontos_onibus, axis = 2) # type: ignore
            relacionamento[nome_linha] = set(np.argmin(distancia, axis = 1))
        return relacionamento
            

    def associar_residencias_a_pontos(self) -> pd.DataFrame:
        """Associa as residências aos pontos de ônibus mais próximos."""
        associacoes = {'residencia': [], 'ponto_onibus': [], 'distancia': []}
        if self.coords_residencias is None or self.coords_pontos_onibus is None:
            raise
        for i, residencia in enumerate(self.coords_residencias):
            distancias = self.distancia_euclidiana(
                residencia.reshape(1, -1), 
                self.coords_pontos_onibus
            )
            idx_ponto_mais_proximo = np.argmin(distancias)
            distancia = distancias[idx_ponto_mais_proximo]
            associacoes['residencia'].append(i)
            associacoes['ponto_onibus'].append(idx_ponto_mais_proximo)
            associacoes['distancia'].append(distancia)
            
        return pd.DataFrame(associacoes)
    
    def _calcular_proporcao_distancia(self, df: pd.DataFrame, limite=400):
        total_residencias = len(df)
        residencias_proximas = df[df['distância'] < limite].shape[0]
        proporcao = residencias_proximas / total_residencias
        return proporcao
    
    def consolidar_associacoes(self) -> pd.DataFrame:
        """
        Consolida todas as associações (linhas, pontos de ônibus e residências).

        Returns:
            list: Lista consolidada com linha, ponto de ônibus, residência e distância.
        """
        try:
            residencias_pontos : pd.DataFrame = self.associar_residencias_a_pontos()
            pontos_linhas = self.associar_ponto_a_linha()
            limite_distancia = 400
            consolidado = {'linha' : [], 'distancia' : [], 'proporcao': []}
            for nome_linha, pontos_onibus_linha in pontos_linhas.items():
                distancias_associadas = residencias_pontos[residencias_pontos['ponto_onibus'].isin(pontos_onibus_linha)]
                
                media_distancia = distancias_associadas['distancia'].mean()
                
                proporcao = (distancias_associadas['distancia'] < limite_distancia).mean()
                
                consolidado['linha'].append(nome_linha)
                consolidado['distancia'].append(media_distancia)
                consolidado['proporcao'].append(proporcao)
                
            return pd.DataFrame(consolidado)
        except Exception as e:
            print(f"Erro ao consolidar as associações: {e}")
            return pd.DataFrame()