map_tools

Biblioteca para manipulação de arquivos geoespaciais e visualização de dados geográficos utilizando folium, geopandas, e outras bibliotecas em Python. Ideal para visualização de rotas, polígonos e dados de transporte em mapas interativos.
Índice

    Instalação
    Funcionalidades
        Carregar Arquivos Geoespaciais
        Filtrar e Manipular Dados Geoespaciais
        Gerar Mapas Interativos
        Adicionar Linhas com Cores Personalizadas
    Exemplo de Uso
    Referências

Instalação

Para instalar a biblioteca map_tools, basta clonar o repositório e instalar as dependências:

bash

git clone <URL-do-repositório>
cd map_tools
pip install -r requirements.txt

Certifique-se de que as bibliotecas necessárias como folium, geopandas, pandas, e fiona estejam corretamente instaladas.
Funcionalidades
Carregar Arquivos Geoespaciais

A biblioteca suporta a leitura de arquivos KML e KMZ. Para trabalhar com arquivos KMZ, eles são convertidos automaticamente para KML:

python

from map_tools import carregar_geospatial_data

gdf = carregar_geospatial_data("caminho_para_arquivo.kml", layer='Nome_da_Camada')

Filtrar e Manipular Dados Geoespaciais

A map_tools permite aplicar filtros diretamente no GeoDataFrame, facilitando a segmentação dos dados:

python

filtered_data = filter_data(gdf, column='Name', value='ativo')

Gerar Mapas Interativos

A biblioteca usa folium para gerar mapas interativos com funcionalidades personalizadas, incluindo a adição de layers e estilos:

python

from map_tools import create_map

m = create_map(gdf, location=[-16.737, -43.8647], zoom_start=12)

Adicionar Linhas com Cores Personalizadas

Adiciona linhas de rotas ao mapa interativo, com opções de cor e opacidade para cada linha:

python

from map_tools import adicionar_linha_ao_mapa

adicionar_linha_ao_mapa(m, 'Nome_da_Linha', geometry, color='#FF5733')

Exemplo de Uso

Abaixo, um exemplo de uso da biblioteca para criar um mapa com dados de linhas de ônibus de uma cidade fictícia:

python

from map_tools import carregar_geospatial_data, create_map, adicionar_linha_ao_mapa, save_map

# Carregar dados geoespaciais

gdf = carregar_geospatial_data("caminho_para_arquivo.kml", layer='Camada_desejada')

# Filtrar dados

gdf_filtered = filter_data(gdf, column='Name', value='ativo')

# Criar o mapa

m = create_map(gdf_filtered, location=[-16.737, -43.8647], zoom_start=12)

# Adicionar linhas de rota

for index, row in gdf_filtered.iterrows():
adicionar_linha_ao_mapa(m, row['Name'], row.geometry, color='blue')

# Salvar o mapa

save_map(m, "meu_mapa_interativo.html")

Referências

    Folium
    Geopandas
    Fiona
