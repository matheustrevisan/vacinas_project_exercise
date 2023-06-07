import mysql.connector
import config

# Conectar ao banco de dados
conn = mysql.connector.connect(
    user=config.user,
    password=config.password,
    host=config.host,
    database='vacinasbd'
)

# Criar cursor para executar comandos SQL
cursor = conn.cursor()

# Adicionar campo à tabela RacaCor
alter_query = "ALTER TABLE Aplicacoes ADD vacina_numDose VARCHAR(10)"
cursor.execute(alter_query)

# Commit das alterações e fechar conexão
conn.commit()
conn.close()
