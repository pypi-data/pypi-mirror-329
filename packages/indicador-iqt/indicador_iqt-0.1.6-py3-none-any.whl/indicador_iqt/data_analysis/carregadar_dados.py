import pandas as pd


def carregar_data(file_path: str) -> pd.DataFrame:
	"""
	Carrega e processa um arquivo CSV contendo dados de horários e datas, realizando as conversões
	necessárias para os tipos datetime.

	Parameters
	----------
	file_path : str
		Caminho completo para o arquivo CSV a ser carregado.

	Returns
	-------
	pd.DataFrame
		DataFrame processado contendo as seguintes colunas:
		- hsstart: datetime - Horário de início
		- hsstop: datetime - Horário de término
		- duracao: timedelta - Duração calculada (hsstop - hsstart)
		- data: datetime - Data inicial
		- dataf: datetime - Data final
		- duracao_minutos: int - Duração em minutos

	Notes
	-----
	O arquivo CSV deve conter as colunas: 'hsstart', 'hsstop', 'data', 'dataf'
	com os seguintes formatos:
	- hsstart, hsstop: "%H:%M:%S"
	- data, dataf: "%d/%m/%Y"
	"""
	df = pd.read_csv(file_path, delimiter=",")

	# Conversões de datetime
	df["hsstart"] = pd.to_datetime(df["hsstart"], format="%H:%M:%S")
	df["hsstop"] = pd.to_datetime(df["hsstop"], format="%H:%M:%S")
	df["duracao"] = df["hsstop"] - df["hsstart"]
	df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
	df["dataf"] = pd.to_datetime(df["dataf"], format="%d/%m/%Y")
	df["duracao_minutos"] = df["duracao"].dt.total_seconds() // 60
	df["duracao_minutos"] = df["duracao_minutos"].astype(int)

	return df


def carregar_integrations(file_path: str) -> pd.Series:
	"""
	Carrega um arquivo CSV de integrações e retorna uma série contendo as linhas de origem únicas.

	Parameters
	----------
	file_path : str
		Caminho completo para o arquivo CSV de integrações.

	Returns
	-------
	pd.Series
		Série contendo valores únicos da coluna 'LINHA ORIGEM'.

	Notes
	-----
	O arquivo CSV deve conter uma coluna chamada 'LINHA ORIGEM'.
	A função remove duplicatas antes de retornar os valores.
	"""
	df_integrations = pd.read_csv(file_path, delimiter=",")
	df_integrations = df_integrations.drop_duplicates(subset=["LINHA ORIGEM"])
	df_integrations = df_integrations["LINHA ORIGEM"]
	return df_integrations


def carregar_planned_trips(file_path: str) -> pd.DataFrame:
	df_rastreamento = pd.read_csv(file_path, delimiter=",")
	colunas_desnecessarias = [
		"'Veiculo Planejado'",
		"Veiculo Real",
		"Motorista",
		"Vel. Media Km",
		"Temp.Ponto",
		"Passageiro",
		"Status da Viagem",
		"Desc. Status da Viagem",
		"Unnamed: 26",
		"Unnamed: 25",
		"Unnamed: 24",
		"Empresa",
		"Tabela",
		"Viagem Editada",
	]

	df_rastreamento_tratado = df_rastreamento.drop(colunas_desnecessarias, axis=1)

	df_rastreamento_tratado[["linha", "sentido"]] = df_rastreamento_tratado[
		"Trajeto"
	].str.extract(r"(\d+)\s*-\s*.*\((ida|volta)\)")

	df_rastreamento_tratado = df_rastreamento_tratado.drop("Trajeto", axis=1)
	df_rastreamento_tratado.replace("-", pd.NA, inplace=True)
	df_rastreamento_tratado["com_horario"] = (
		df_rastreamento_tratado[["Chegada ao ponto", "Partida Real", "Chegada Real"]]
		.notna()
		.any(axis=1)
	)
	agrupado = (
		df_rastreamento_tratado.groupby(["linha", "sentido"])["com_horario"]
		.value_counts(normalize=False)
		.unstack(fill_value=0)
	)

	# # Renomeia as colunas para maior clareza
	agrupado.columns = ["sem_horario", "com_horario"]

	# # Calcula a proporção de viagens sem horário sobre o total de viagens para cada grupo
	agrupado["proporcao_sem_horario"] = agrupado["com_horario"] / (
		agrupado["sem_horario"] + agrupado["com_horario"]
	)

	return agrupado
