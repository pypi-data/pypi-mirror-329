import folium
import geopandas as gpd
from folium.plugins import Fullscreen, GroupedLayerControl

from ..data_analysis.classificar_indicadores import ClassificarIndicadores
from .camadas import adicionar_linha_ao_mapa, adicionar_linha_ao_mapa_sem_grupo


class MapaIQT:
    def __init__(self, gdf_city: gpd.GeoDataFrame):
        """
        Inicializa um mapa centrado na cidade com uma camada base de bairros.
        """
        self.gdf_city = gdf_city
        self.mapa = self._inicializar_mapa(self.gdf_city)
        self.legenda = ""

    def _inicializar_mapa(self, gdf_city: gpd.GeoDataFrame) -> folium.Map:
        """
        Inicializa um mapa Folium centrado na cidade com uma camada base de bairros.

        Parameters
        ----------
        gdf_city : gpd.GeoDataFrame
            GeoDataFrame contendo as geometrias dos bairros da cidade.
            Deve conter uma coluna 'geometry' com os polígonos dos bairros.

        Returns
        -------
        folium.Map
            Mapa Folium inicializado com:
            - Camada base CartoDB Voyager
            - Zoom inicial de 12
            - Camada de bairros estilizada
            - Centrado no centroide médio da cidade

        Notes
        -----
        O estilo dos bairros é definido com:
        - Preenchimento branco (fillColor: white)
        - Borda preta fina (color: black, weight: 0.7)
        - Transparência de 50% (fillOpacity: 0.5)

        Example
        -------
        >>> gdf_city = gpd.read_file('caminho/para/bairros.geojson')
        >>> mapa = inicializar_mapa(gdf_city)
        >>> mapa.save('mapa_cidade.html')
        """
        # Define centro do mapa

        bounds = gdf_city.total_bounds  # [minx, miny, maxx, maxy]

        # Calcula o centro do mapa
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2

        # map_center = [gdf_city.geometry.centroid.y.mean(), gdf_city.geometry.centroid.x.mean()]
        map_routes = folium.Map(
            location=[center_lat, center_lon], zoom_start=12, tiles="CartoDB Voyager"
        )

        folium.GeoJson(
            gdf_city,
            style_function=lambda feature: {
                "fillColor": "white",
                "color": "black",
                "weight": 0.7,
                "fillOpacity": 0.5,
            },
            name="Bairros",
        ).add_to(map_routes)

        map_routes.fit_bounds(
            [
                [bounds[1], bounds[0]],  # [lat_min, lon_min]
                [bounds[3], bounds[2]],  # [lat_max, lon_max]
            ]
        )

        # Adiciona controle de zoom
        Fullscreen().add_to(map_routes)

        return map_routes

    def classificar_rota(self, gdf_routes: gpd.GeoDataFrame) -> folium.Map:
        """
        Adiciona rotas classificadas ao mapa base.

        Parameters
        ----------
        map_routes : folium.Map
            Mapa Folium base onde as rotas serão adicionadas.
            Geralmente é o mapa retornado por inicializar_mapa().

        gdf_routes : gpd.GeoDataFrame
            GeoDataFrame contendo as rotas a serem adicionadas.
            Deve conter as seguintes colunas:
            - geometry: geometria do tipo LineString
            - linha: nome da rota para o tooltip
            - iqt: índice de qualidade para determinação da cor

        Returns
        -------
        folium.Map
            Mapa Folium com as rotas adicionadas e classificadas por cor
            de acordo com o IQT.

        Notes
        -----
        - Cada rota é adicionada individualmente ao mapa usando adicionar_linha_ao_mapa_sem_grupo
        - A classificação por cores é determinada pelo valor do IQT de cada rota
        - As cores são definidas pela função color_iqt (importada indiretamente
        através de adicionar_linha_ao_mapa_sem_grupo)

        Example
        -------
        >>> gdf_city = gpd.read_file('caminho/para/bairros.geojson')
        >>> gdf_routes = gpd.read_file('caminho/para/rotas.geojson')
        >>> mapa = inicializar_mapa(gdf_city)
        >>> mapa_final = classificar_rota(mapa, gdf_routes)
        >>> mapa_final.save('mapa_rotas.html')
        """
        for index, line in gdf_routes.iterrows():
            # line_dict = line.to_dict()  # Converte a linha para um dicionário
            adicionar_linha_ao_mapa_sem_grupo(line, self.mapa)
        return self.mapa

    def classificar_rota_grupo(self, gdf_routes: gpd.GeoDataFrame) -> folium.Map | None:
        """
        Adiciona rotas classificadas ao mapa base.

        Parameters
        ----------
        map_routes : folium.Map
            Mapa Folium base onde as rotas serão adicionadas.
            Geralmente é o mapa retornado por inicializar_mapa().

        gdf_routes : gpd.GeoDataFrame
            GeoDataFrame contendo as rotas a serem adicionadas.
            Deve conter as seguintes colunas:
            - geometry: geometria do tipo LineString
            - linha: nome da rota para o tooltip
            - iqt: índice de qualidade para determinação da cor

        Returns
        -------
        folium.Map
            Mapa Folium com as rotas adicionadas e classificadas por cor
            de acordo com o IQT.

        Notes
        -----
        - Cada rota é adicionada individualmente ao mapa usando adicionar_linha_ao_mapa_sem_grupo
        - A classificação por cores é determinada pelo valor do IQT de cada rota
        - As cores são definidas pela função color_iqt (importada indiretamente
        através de adicionar_linha_ao_mapa_sem_grupo)

        Example
        -------
        >>> gdf_city = gpd.read_file('caminho/para/bairros.geojson')
        >>> gdf_routes = gpd.read_file('caminho/para/rotas.geojson')
        >>> mapa = inicializar_mapa(gdf_city)
        >>> mapa_final = classificar_rota(mapa, gdf_routes)
        >>> mapa_final.save('mapa_rotas.html')
        """
        grupos = {}
        classificador = ClassificarIndicadores()
        listas_grupo = []
        for index, line in gdf_routes.iterrows():
            classificao_iqt = classificador.classificacao_iqt_pontuacao(line.iqt)

            grupo = grupos.get(classificao_iqt, None)
            if grupo is None:
                grupo = folium.FeatureGroup(name=classificao_iqt)
                listas_grupo.append(grupo)
                self.mapa.add_child(grupo)
                grupos[classificao_iqt] = grupo
            adicionar_linha_ao_mapa(line, grupo)

        GroupedLayerControl(
            groups={"classificacao": listas_grupo},
            collapsed=False,
        ).add_to(self.mapa)