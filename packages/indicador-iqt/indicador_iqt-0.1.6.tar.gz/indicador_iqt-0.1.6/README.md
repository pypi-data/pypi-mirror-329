# 📊 Indicadores IQT - Biblioteca para Avaliação da Qualidade do Transporte Público

Esta biblioteca tem como objetivo automatizar o cálculo do **Índice de Qualidade do Transporte (IQT)**, baseado nos critérios estabelecidos no artigo **"MESTRADO INDICADOR DE QUALIDADE PARA AVALIAR TRANSPORTE COLETIVO URBANO"**. O IQT é uma métrica essencial para a análise e otimização do transporte público, considerando fatores como pontualidade, frequência de atendimento, cumprimento de itinerários e infraestrutura.

---

## 📦 **Instalação**

Antes de utilizar a biblioteca, certifique-se de instalar as dependências necessárias:

```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

🔹 1. Importação da Biblioteca

```python
from indicador_iqt import CalcularIndicadores
```

🔹 2. Inicializando a Classe

```python
calc = CalcularIndicadores()
```

🔹 3. Carregando os Dados

Os dados podem ser carregados a partir de um `pandas.DataFrame` ou `geopandas.GeoDataFrame`:

```python
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

# Exemplo de dados fictícios de linhas de ônibus
linhas_df = gpd.GeoDataFrame({
    'linha': ['101', '102'],
    'geometry': [LineString([(0, 0), (1, 1), (2, 2)]), LineString([(3, 3), (4, 4), (5, 5)])]
})

# Carregar os dados na classe
calc.load_dados_linha(linhas_df)
```

🔹 4. Cálculo de Indicadores

A biblioteca suporta o cálculo de diversos indicadores de qualidade do transporte, como:

```python
# Cálculo do tempo médio de operação
tempo_medio = calc.frequencia_atendimento_pontuacao(df_frequencia)
print(tempo_medio)

# Cálculo da pontualidade
pontualidade = calc.calcular_pontualidade(df_pontualidade)
print(pontualidade)

# Cálculo do cumprimento de itinerário
cumprimento = calc.cumprimento_itinerario(df_cumprimento)
print(cumprimento)
```

🔹 5. Cálculo do Índice IQT

```python
linha_indicadores = [0.8, 0.7, 0.6, 0.9, 0.85, 0.75, 0.65, 0.7, 0.5, 0.6]
iqt = calc.calcular_iqt(linha_indicadores)
print(f"Índice IQT: {iqt}")
```

| Método                                 | Descrição                                                   |
| -------------------------------------- | ----------------------------------------------------------- |
| `load_dados_linha(df)`                 | Carrega os dados das linhas e converte WKT para LineString. |
| `frequencia_atendimento_pontuacao(df)` | Calcula o tempo médio de operação por rota.                 |
| `calcular_pontualidade(df)`            | Calcula a pontuação para o indicador de pontualidade.       |
| `cumprimento_itinerario(df)`           | Calcula o cumprimento de itinerário por quilometragem.      |
| `calcular_iqt(lista_indicadores)`      | Calcula o Índice de Qualidade do Transporte (IQT).          |
| `processar_iqt()`                      | Processa os cálculos do IQT e gera classificações.          |

## 🤝 Contribuindo

### Contribuições são bem-vindas! Para contribuir:

- Fork o repositório.
- Crie uma branch `(feature/nova-funcionalidade)`.
- Faça suas alterações e commit `(git commit -m "Adiciona nova funcionalidade")`.
- Envie um Pull Request.

### 📜 Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
👨‍💻 Autor

Desenvolvido por Yago Maia - GitHub: https://github.com/YagoMaia
