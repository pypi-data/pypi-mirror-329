import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


class Graficos:
    """
    Classe para gerar gráficos com seaborn.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def plot_boxplot_passageiros_por_rota(self):
        """Plota um boxplot da distribuição de passageiros por rota.

        Args:
            self.df (pd.DataFrame): DataFrame contendo a coluna 'linha' para as rotas e 'qtpsg' para a quantidade de passageiros.

        Returns:
            None: A função exibe o gráfico, mas não retorna nenhum valor.

        Example:
            >>> plot_boxplot_passageiros_por_rota(self.df)
        """
        plt.figure(figsize=(12, 6))
        # media_passageiros_por_rota = self.df.groupby('linha')['qtpsg'].mean().sort_values()
        sns.boxplot(x="qtpsg", y="linha", data=self.df, hue="linha")
        plt.title("Distribuição de Passageiros por Rota")
        plt.xlabel("Número de Passageiros")
        plt.ylabel("Rotas")
        plt.xticks(rotation=45)
        plt.show()

    def plot_boxplot_valores_arrecadados_por_rota(self):
        """Plota um boxplot da distribuição dos valores arrecadados por rota.

        Args:
            self.df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar as rotas e 'valor_jornada' para os valores arrecadados.

        Returns:
            None: A função exibe o gráfico, mas não retorna nenhum valor.

        Example:
            >>> plot_boxplot_valores_arrecadados_por_rota(self.df)
        """
        plt.figure(figsize=(12, 6))
        # valor_arrecadado_por_rota = self.df.groupby('linha')['valor_jornada']
        sns.boxplot(x="valor_jornada", y="linha", data=self.df, hue="linha")
        plt.title("Distribuição dos Valores Arrecadados por Rota")
        plt.ylabel("Rota")
        plt.xlabel("Valor Arrecadado")
        plt.xticks(rotation=45)
        plt.show()

    def plot_duracao_medio_por_mes(self):
        """Plota um boxplot da distribuição do tempo de viagem por rota.

        Args:
            self.df (pd.DataFrame): DataFrame contendo a coluna 'linha' para identificar as rotas e 'duracao' para a duração das viagens em minutos.

        Returns:
            None: A função exibe o gráfico, mas não retorna nenhum valor.

        Example:
            >>> plot_duracao_medio_por_mes(self.df)
        """
        plt.figure(figsize=(12, 6))
        # tempo_medio_operacao = self.df.groupby('linha')['duracao']
        sns.boxplot(x="duracao", y="linha", data=self.df, hue="linha")
        plt.title("Distribuição de Tempo de Viagem")
        plt.xlabel("Tempo de Duração")
        plt.ylabel("Rotas")
        plt.show()

    # def plot_histograma_passageiros(self):
    #     """Plota o histograma da distribuição de passageiros."""
    #     plt.figure(figsize=(10, 6))
    #     qtpsg_numeric = pd.to_numeric(self.df['qtpsg'], errors='coerce').astype(float)
    #     sns.histplot(qtpsg_numeric, kde=True)
    #     plt.title('Distribuição de Passageiros')
    #     plt.xlabel('Número de Passageiros')
    #     plt.ylabel('Frequência')
    #     plt.show()

    def plot_media_passageiros_por_rota(self):
        """Plota o gráfico de barras da média de passageiros por rota."""
        media_passageiros = self.df.groupby("linha")["qtpsg"].mean().sort_values()
        plt.figure(figsize=(10, 6))
        media_passageiros.plot(kind="bar", color="skyblue")
        plt.title("Média de Passageiros por Rota")
        plt.xlabel("Rota")
        plt.ylabel("Média de Passageiros")
        plt.xticks(rotation=45)
        plt.show()

    def plot_duracao_vs_valor(self):
        """Plota um gráfico de dispersão entre duração da viagem e valores arrecadados."""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x="duracao", y="valor_jornada", data=self.df, hue="linha")
        plt.title("Duração vs Valor Arrecadado por Rota")
        plt.xlabel("Duração da Viagem (minutos)")
        plt.ylabel("Valor Arrecadado")
        plt.show()

    def plot_tendencia_passageiros(self):
        """Plota a tendência do número de passageiros ao longo do tempo."""
        # self.df['data'] = pd.to_datetime(self.df['data'], dayfirst=True)  # Certifique-se de ter uma coluna 'data'
        df_grouped = self.df.groupby(self.df["data"].dt.to_period("M"))["qtpsg"].sum()
        plt.figure(figsize=(12, 6))
        df_grouped.plot(kind="line", color="green")
        plt.title("Tendência de Passageiros por Mês")
        plt.xlabel("Mês")
        plt.ylabel("Número Total de Passageiros")
        plt.show()

    def plot_barras_empilhadas(self):
        """Plota gráfico de barras empilhadas de passageiros por mês e por rota."""
        # self.df['data'] = pd.to_datetime(self.df['data'], dayfirst=True)
        self.df["mes"] = self.df["data"].dt.to_period("M")
        self.df_pivot = self.df.pivot_table(
            index="mes", columns="linha", values="qtpsg", aggfunc="sum"
        )
        self.df_pivot.plot(kind="bar", stacked=True, figsize=(12, 6))
        plt.title("Passageiros por Mês e Rota")
        plt.xlabel("Mês")
        plt.ylabel("Total de Passageiros")
        plt.show()

    def plot_area_passageiros(self):
        """Plota um gráfico de área para a evolução do número de passageiros."""
        # self.df['data'] = pd.to_datetime(self.df['data'], dayfirst=True)
        self.df_grouped = (
            self.df.groupby([self.df["data"].dt.to_period("M"), "linha"])["qtpsg"]
            .sum()
            .unstack()
            .fillna(0)
        )
        self.df_grouped.plot(kind="area", stacked=True, figsize=(12, 6))
        plt.title("Evolução de Passageiros por Rota ao Longo do Tempo")
        plt.xlabel("Mês")
        plt.ylabel("Total de Passageiros")
        plt.show()

    def plotar_graficos(self):
        self.plot_area_passageiros()
        self.plot_boxplot_passageiros_por_rota()
        self.plot_boxplot_valores_arrecadados_por_rota()
        # self.plot_histograma_passageiros()
        self.plot_media_passageiros_por_rota()
        self.plot_duracao_vs_valor()
        self.plot_tendencia_passageiros()
        self.plot_barras_empilhadas()
        # self.plot_violin_passageiros_por_rota()
        # self.plot_heatmap_correlacao()
        self.plot_duracao_medio_por_mes()
