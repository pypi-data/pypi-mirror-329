import pandas as pd
import pytest

from indicador_iqt.data_analysis.calcular_indicadores import CalcularIndicadores


@pytest.fixture
def calculator():
    """
    Fixture para criar uma instância da classe CalcularIndicadores.
    """
    return CalcularIndicadores()


@pytest.fixture
def sample_lines():
    """
    Fixture para criar um DataFrame de linhas fictícias.
    """
    data = {
        "linha": ["1501", "4601"],
        "geometry": [
            "LINESTRING (-43.88156644059743 -16.70073765826833, -43.88142926517379 -16.69999706663925, -43.8820968983508 -16.69988680484133)",
            "LINESTRING (-43.88190489230887 -16.69899957081534, -43.88129594299133 -16.69831881961529, -43.88098272312113 -16.69838557938928)",
        ],
        "via_pavimentada": [1, 1],
        "integracao": ["Integração tarifária temporal", "Integração parcial"],
        "treinamento_motorista": [1, 1],
        "informacao_internet": ["Sistema online", "Sistema básico"],
        "valor_tarifa": ["Aumento regular", "Aumento equivalente"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_frequencia_atendimento_pontuacao():
    """
    Fixture para criar um DataFrame de frequência de atendimento.
    """
    data = {
        "empresa": [1, 2, 3],
        "linha": ["4601", "4601", "4601"],
        "hsstart": ["06:07:57", "06:07:59", "06:10:59"],
        "hsstop": ["06:10:57", "06:15:59", "06:19:59"],
        "data": ["01/01/2024", "01/01/2024", "01/01/2024"],
        "dataf": ["01/01/2024", "01/01/2024", "01/01/2024"],
        "qtpsg": [13, 11, 9],
        "valor_jornada": [13, 11, 9],
        "sentido": [1, 0, 0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_pontualidade():
    """
    Fixture para criar um DataFrame fictício para teste de pontualidade.
    """
    data = {
        "Data": ["01/01/2024", "01/01/2024"],
        "Trajeto": ["4601 - Rota Principal (ida)", "4601 - Rota Principal (volta)"],
        "Chegada ao ponto": ["05:34:26", "-"],
        "Partida Real": ["00:42:00", "-"],
        "Chegada Real": ["05:52:00", "-"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_cumprimento():
    """
    Fixture para criar um DataFrame fictício para teste de cumprimento.
    """
    data = {
        "Data": ["01/01/2024", "01/01/2024"],
        "Trajeto": ["4601 - Rota Principal (ida)", "4601 - Rota Principal (volta)"],
        "KM Executado": [18, 17],
    }
    return pd.DataFrame(data)


def test_carregar_dados_linha(calculator, sample_lines):
    """
    Testa o método `carregar_dados_linha` para carregar linhas.
    """
    loaded_lines = calculator.carregar_dados_linha(sample_lines)

    assert not loaded_lines.empty, "O DataFrame de linhas não deveria estar vazio"
    assert "linha" in loaded_lines.columns, "A coluna 'linha' deve estar presente"
    assert loaded_lines.geometry.geom_type.eq("LineString").all(), (
        "Todas as geometrias devem ser LineStrings"
    )


def test_carregar_cumprimento(calculator, sample_cumprimento):
    """
    Testa o método `carregar_cumprimento` para carregar cumprimento.
    """
    cumprimento = calculator.carregar_cumprimento(sample_cumprimento)

    assert not cumprimento.empty, "O DataFrame de cumprimento não deveria estar vazio"
    assert "linha" in cumprimento.columns, "A coluna 'trajeto' deve estar presente"
    assert "KM Executado" in cumprimento.columns, (
        "A coluna 'cumprimento' deve estar presente"
    )


def test_carregar_frequencia_atendimento_pontuacao(
    calculator, sample_frequencia_atendimento_pontuacao
):
    """
    Testa o método `carregar_frequencia_atendimento_pontuacao` para carregar frequência de atendimento.
    """
    frequencia = calculator.carregar_frequencia_atendimento_pontuacao(
        sample_frequencia_atendimento_pontuacao
    )

    assert not frequencia.empty, "O DataFrame de frequência não deveria estar vazio"
    assert "linha" in frequencia.columns, "A coluna 'linha' deve estar presente"
    assert "frequencia_atendimento_pontuacao" in frequencia.columns, (
        "A coluna 'frequencia_atendimento_pontuacao' deve estar presente"
    )


def test_calcular_pontualidade(calculator, sample_pontualidade):
    """
    Testa o método `calcular_pontualidade` para calcular a pontualidade.
    """
    pontualidade = calculator.calcular_pontualidade(sample_pontualidade)

    assert not pontualidade.empty, "O DataFrame de pontualidade não deveria estar vazio"
    assert "linha" in pontualidade.columns, "A coluna 'linha' deve estar presente"
    assert "pontualidade" in pontualidade.columns, (
        "A coluna 'pontualidade' deve estar presente"
    )


def test_cumprimento_itinerario(calculator, sample_cumprimento):
    """
    Testa o método `cumprimento_itinerario` para calcular o cumprimento.
    """
    cumprimento = calculator.cumprimento_itinerario(sample_cumprimento)

    assert not cumprimento.empty, "O DataFrame de cumprimento não deveria estar vazio"
    assert "linha" in cumprimento.columns, "A coluna 'linha' deve estar presente"
    assert "KM Executado" in cumprimento.columns, (
        "A coluna 'KM Executado' deve estar presente"
    )


def test_calcular_iqt(calculator):
    """
    Testa o método `calcular_iqt` para calcular o Índice de Qualidade do Transporte.
    """
    # Criando uma lista de valores de indicadores
    indicadores = [1, 0.8, 0.9, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

    iqt = calculator.calcular_iqt(indicadores)

    assert isinstance(iqt, float), (
        "O resultado do IQT deve ser um número de ponto flutuante"
    )


def test_carregar_dados(
    calculator,
    sample_lines,
    sample_frequencia_atendimento_pontuacao,
    sample_pontualidade,
    sample_cumprimento,
):
    """
    Testa o método `carregar_dados` com todos os DataFrames.
    """
    calculator.carregar_dados(
        sample_lines,
        sample_frequencia_atendimento_pontuacao,
        sample_pontualidade,
        sample_cumprimento,
    )

    assert not calculator.dados_linhas.empty, "Dados de linhas não carregados"
    assert not calculator.frequencia.empty, "Dados de frequência não carregados"
    assert not calculator.pontualidade.empty, "Dados de pontualidade não carregados"
    assert not calculator.cumprimento.empty, "Dados de cumprimento não carregados"
