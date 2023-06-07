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

# Adicionar valores à tabela RacaCor
insert_query = "INSERT IGNORE INTO RacaCor (raca_cor_codigo, raca_cor_valor) VALUES (%s, %s)"

values = [
    ("1", 'Branca'),
    ("2", 'Preta'),
    ("3", 'Parda'),
    ("4", 'Amarela'),
    ("99", 'Sem informação')
]

cursor.executemany(insert_query, values)

# Commit das alterações e fechar conexão
conn.commit()
conn.close()
