import requests
import pandas as pd
from mysql.connector import connect, Error
from config import user, password, host, database


# Def para fazer a requisição, retorna o resultado normalizado em um dataframe e a variavel scroll_id que inicia a proxima requisição
def fetch_data_from_api(url, credentials, params, headers, req):
	try:
		if req == 1:
			response = requests.get(url, auth=credentials, json=params, headers=headers)
			print(str(url)+"\n"+str(credentials)+"\n"+str(params)+"\n"+str(headers))
		else:
			response = requests.get(url, auth=credentials, json=params, headers=headers)
			print(str(url)+"\n"+str(credentials)+"\n"+str(params)+"\n"+str(headers))
		print(response)
		data = response.json()
		hits = data.get("hits", {}).get("hits", [])
		#hits = data["hits"]["hits"]
		normalized_hits = [hit["_source"] for hit in hits]
		scroll_id = data.get("_scroll_id", "")
		
		# Normalize os dados da resposta em um dataframe
		df = pd.json_normalize(normalized_hits)

		
		return df, scroll_id

	except requests.exceptions.RequestException as e:
		print(e)


# Função para inserir os dados no banco de dados
def insert_data(defs):
	try:
		connection = connect(user=user, password=password, host=host, database=database)
		cursor = connection.cursor()
		
		
		for lista in defs:
			table_name = lista[0]
			df = lista[1]
			# Gere o SQL de inserção com base no dataframe
			placeholders = ",".join(["%s"] * len(df.columns))
			insert_sql = f"INSERT IGNORE INTO {table_name} ({','.join(df.columns)}) VALUES ({placeholders})"

			
			# Converta o dataframe para uma lista de tuplas para inserção
			data = [tuple(x) for x in df.to_numpy()]

			# Execute a inserção
			cursor.executemany(insert_sql, data)
			connection.commit()

			print(f"{len(data)} registros inseridos na tabela {table_name}")

	except Error as e:
		print(e)

	finally:
		if cursor:
			cursor.close()
		if connection and connection.is_connected():
			connection.close()


# Função para obter o tamanho de armazenamento atual do banco de dados
def check_storage_size():
	try:
		connection = connect(user=user, password=password, host=host, database=database)
		cursor = connection.cursor()

		# Execute a consulta para obter o tamanho do armazenamento
		cursor.execute("SELECT SUM(data_length + index_length) / 1024 / 1024 / 1024 AS size_gb FROM information_schema.tables WHERE table_schema = %s GROUP BY table_schema", (database,))
		result = cursor.fetchone()

		if result:
			storage_size_gb = result[0]
			print(f"Tamanho de armazenamento atual: {storage_size_gb:.2f} GB")

			return storage_size_gb

	except Error as e:
		print(e)

	finally:
		if cursor:
			cursor.close()
		if connection and connection.is_connected():
			connection.close()


# Função principal para executar o código
def main():
	url = "https://imunizacao-es.saude.gov.br/_search?scroll=1m"
	credentials = ("imunizacao_public", "qlto5t&7r_@+#Tlstigi")
	headers = {"Content-Type": "application/json"}
	params = {"size": 10000}
	primary_keys = []  # Armazene as chaves primárias aqui
	requisicao = 1
	while True:
		print("-------------------Começo do loop----------------------")
		# Faça a requisição à API do datasus
		df, scroll_id = fetch_data_from_api(url, credentials, params, headers, requisicao)
		requisicao +=1

		print(len(df))
		print(df.columns)
		print(df['paciente_racaCor_codigo'])
		df['raca_cor_codigo'] = df['paciente_racaCor_codigo']
		df['municipio_codigo'] = df['paciente_endereco_coIbgeMunicipio']
		# Dicionário de mapeamento dos nomes das colunas
		column_mapping = {
			'paciente_endereco_coPais': 'coPais',
			'paciente_endereco_nmPais': 'nmPais',
			'raca_cor_codigo': 'raca_cor_codigo',
			'paciente_racaCor_codigo': 'paciente_racaCor_codigo',
			'paciente_racaCor_valor': 'raca_cor_valor',
			'paciente_endereco_coIbgeMunicipio': 'paciente_endereco_colbgeMunicipio',
			'municipio_codigo': 'municipio_codigo',
			'paciente_endereco_nmMunicipio': 'municipio_nome',
			'paciente_endereco_uf': 'uf_sigla',
			'estabelecimento_valor': 'estabelecimento_valor',
			'estabelecimento_razaoSocial': 'estabelecimento_razaoSocial',
			'estalecimento_noFantasia': 'estabelecimento_noFantasia',
			'estabelecimento_municipio_codigo': 'estabelecimento_municipio_codigo',
			'vacina_grupoAtendimento_codigo': 'vacina_grupo_atendimento_code',
			'vacina_grupoAtendimento_nome': 'vacina_grupo_atendimento_nome',
			'vacina_categoria_codigo': 'vacina_categoria_code',
			'vacina_categoria_nome': 'vacina_categoria_nome',
			'vacina_fabricante_referencia': 'vacina_fabricante_referencia',
			'vacina_fabricante_nome': 'vacina_fabricante_nome',
			'vacina_codigo': 'vacina_codigo',
			'vacina_lote': 'vacina_lote',
			'vacina_nome': 'vacina_nome',
			'paciente_id': 'paciente_id',
			'paciente_dataNascimento': 'paciente_data_nascimento',
			'paciente_enumSexoBiologico': 'paciente_enumSexoBiologico',
			'paciente_endereco_cep': 'paciente_endereco_cep',
			'paciente_nacionalidade_enumNacionalidade': 'paciente_nacionalidade_enumNacionalidade',
			'': 'aplicacao_id',
			'document_id': 'document_id',
			'vacina_dataAplicacao': 'vacina_data_aplicacao',
			'sistema_origem': 'sistema_origem',
			'vacina_numDose': 'vacina_numDose',
			'vacina_descricao_dose': 'vacina_descricao_dose',
		}

		# Renomear as colunas do DataFrame
		df.rename(columns=column_mapping, inplace=True)
		
		
		df_pais = df[['coPais','nmPais']].drop_duplicates()
		df_racaCor = df[['raca_cor_codigo', 'raca_cor_valor']].drop_duplicates()
		df_municipio = df[['municipio_codigo', 'municipio_nome', 'uf_sigla', 'coPais', ]].drop_duplicates()
		df_estabelecimento = df[['estabelecimento_valor', 'estabelecimento_razaoSocial', 'estabelecimento_noFantasia', 'estabelecimento_municipio_codigo']].drop_duplicates()
		df_VacinaGrupoAtendimento = df[['vacina_grupo_atendimento_code','vacina_grupo_atendimento_nome']].drop_duplicates()
		df_CategoriaVacina = df[['vacina_categoria_code','vacina_categoria_nome']].drop_duplicates()
		df_FabricanteVacina = df[['vacina_fabricante_referencia', 'vacina_fabricante_nome']].drop_duplicates()
		df_Vacina = df[['vacina_codigo', 'vacina_lote', 'vacina_fabricante_referencia','vacina_grupo_atendimento_code', 'vacina_categoria_code', 'vacina_nome']].drop_duplicates()
		df_Paciente = df[['paciente_id', 'paciente_data_nascimento', 'paciente_enumSexoBiologico', 'paciente_racaCor_codigo', 'paciente_endereco_colbgeMunicipio', 'paciente_endereco_cep', 'paciente_nacionalidade_enumNacionalidade']].drop_duplicates()
		df_Aplicacoes = df[['paciente_id', 'estabelecimento_valor', 'vacina_codigo', 'sistema_origem', 'vacina_data_aplicacao', 'vacina_descricao_dose', 'document_id', 'vacina_numDose']].drop_duplicates()
		defs = [["Paises",df_pais], ["RacaCor",df_racaCor], ["Municipio",df_municipio], ["Estabelecimento",df_estabelecimento], ["VacinaGrupoAtendimento",df_VacinaGrupoAtendimento], ["CategoriaVacina",df_CategoriaVacina], ["FabricanteVacina",df_FabricanteVacina], ["Vacina", df_Vacina], ["Paciente", df_Paciente], ["Aplicacoes", df_Aplicacoes]]

       
		
		# Inserir os dados no banco de dados
		insert_data(defs)

		# Limpe os dados na memória
		del df, defs, df_pais, df_racaCor, df_municipio, df_estabelecimento, df_VacinaGrupoAtendimento, df_CategoriaVacina, df_FabricanteVacina, df_Vacina, df_Paciente, df_Aplicacoes 

		# Verifique o tamanho de armazenamento atual
		storage_size_gb = check_storage_size()

		# Verifique se o tamanho de armazenamento excede 12GB
		if storage_size_gb and storage_size_gb > 12:
			break

		# Atualize os parâmetros para a próxima requisição
		url = "https://imunizacao-es.saude.gov.br/_search/scroll"
		params = {"scroll_id": scroll_id, "scroll": "1m"}

		# Verifique se não há mais resultados
		if not scroll_id:
			break



# Executar a função principal
main()
