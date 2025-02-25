import matplotlib.pyplot as plt
import pandas as pd
import pytest

from indicador_iqt.data_analysis.visualizar_graficos import Graficos


@pytest.fixture
def sample_dataframe():
    """Fixture to create a sample DataFrame for testing."""
    data = {
        "empresa": [1, 1, 1, 1, 1],
        "uds_id": [6220486, 6220486, 6220486, 6220486, 6220486],
        "data": ["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01"],
        "dataf": ["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01"],
        "sentido": [0, 0, 0, 0, 1],
        "linha": [4601, 4601, 4601, 4601, 4601],
        "carro": [20103, 20103, 20103, 20103, 20103],
        "qtpsg": [3, 2, 5, 1, 2],
        "valor_jornada": [12.0, 0.0, 20.0, 4.0, 8.0],
        "nao_sei": [75.0, 0.0, 0.0, 0.0, 5.0],
        "duracao": [49.9, 49.9, 49.9, 49.9, 52.983333],
    }
    return pd.DataFrame(data)


@pytest.fixture
def graficos_instance(sample_dataframe):
    """Fixture to create a Graficos instance with sample data."""
    # Add duration column for methods requiring it
    # sample_dataframe['duracao_minutos'] = (pd.to_datetime(sample_dataframe['hsstop']) -
    #                                         pd.to_datetime(sample_dataframe['hsstart'])).dt.total_seconds() / 60
    sample_dataframe["data"] = pd.to_datetime(sample_dataframe["data"])
    return Graficos(sample_dataframe)


def test_plot_boxplot_passageiros_por_rota(graficos_instance):
    """Test boxplot of passengers by route."""
    try:
        graficos_instance.plot_boxplot_passageiros_por_rota()
        plt.close()
    except Exception as e:
        pytest.fail(f"Boxplot test failed: {e}")


def test_plot_boxplot_valores_arrecadados_por_rota(graficos_instance):
    """Test boxplot of collected values by route."""
    try:
        graficos_instance.plot_boxplot_valores_arrecadados_por_rota()
        plt.close()
    except Exception as e:
        pytest.fail(f"Valores arrecadados boxplot test failed: {e}")


def test_plot_duracao_medio_por_mes(graficos_instance):
    """Test boxplot of average trip duration."""
    try:
        graficos_instance.plot_duracao_medio_por_mes()
        plt.close()
    except Exception as e:
        pytest.fail(f"Duração médio por mês test failed: {e}")


def test_plot_histograma_passageiros(graficos_instance):
    """Test histogram of passengers."""
    try:
        graficos_instance.plot_histograma_passageiros()
        plt.close()
    except Exception as e:
        pytest.fail(f"Histograma de passageiros test failed: {e}")


def test_plot_media_passageiros_por_rota(graficos_instance):
    """Test bar plot of average passengers by route."""
    try:
        graficos_instance.plot_media_passageiros_por_rota()
        plt.close()
    except Exception as e:
        pytest.fail(f"Média de passageiros por rota test failed: {e}")


def test_plot_duracao_vs_valor(graficos_instance):
    """Test scatter plot of trip duration vs collected value."""
    try:
        graficos_instance.plot_duracao_vs_valor()
        plt.close()
    except Exception as e:
        pytest.fail(f"Duração vs valor test failed: {e}")


def test_plot_tendencia_passageiros(graficos_instance):
    """Test line plot of passenger trend."""
    try:
        graficos_instance.plot_tendencia_passageiros()
        plt.close()
    except Exception as e:
        pytest.fail(f"Tendência de passageiros test failed: {e}")


def test_plot_barras_empilhadas(graficos_instance):
    """Test stacked bar plot of passengers."""
    try:
        graficos_instance.plot_barras_empilhadas()
        plt.close()
    except Exception as e:
        pytest.fail(f"Barras empilhadas test failed: {e}")


def test_plot_area_passageiros(graficos_instance):
    """Test area plot of passengers."""
    try:
        graficos_instance.plot_area_passageiros()
        plt.close()
    except Exception as e:
        pytest.fail(f"Área de passageiros test failed: {e}")


def test_plotar_graficos(graficos_instance):
    """Test plotting all graphics at once."""
    try:
        graficos_instance.plotar_graficos()
        plt.close("all")
    except Exception as e:
        pytest.fail(f"Plotar gráficos test failed: {e}")
