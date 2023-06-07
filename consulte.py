import mysql.connector
import config

# Conectar ao banco de dados
conn = mysql.connector.connect(
    user=config.user,
    password=config.password,
    host=config.host,
    database=config.database
)

# Criar cursor para executar comandos SQL
cursor = conn.cursor()

# Consultar os valores da tabela RacaCor
cursor.execute("SELECT DISTINCT vacina_data_aplicacao FROM Aplicacoes ORDER BY vacina_data_aplicacao DESC LIMIT 5")
#cursor.execute("SELECT * FROM RacaCor")
#cursor.execute("SELECT * FROM Paises")

# Obter todos os registros retornados pela consulta
result = cursor.fetchall()

# Exibir os valores retornados
for row in result:
    print(str(row[0])[:10])

# Fechar conexão
conn.close()
