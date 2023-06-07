import mysql.connector
import config

# Conectar ao banco de dados
conn = mysql.connector.connect(
    user=config.user,
    password=config.password,
    host=config.host,
    database= config.database
)

# Criar cursor para executar comandos SQL
cursor = conn.cursor()

# Consultar as tabelas do banco de dados
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'vacinasbd'")
tables = cursor.fetchall()

# Exibir as tabelas e seus campos
for table in tables:
    table_name = table[0]
    print("Tabela:", table_name)
    
    # Consultar os campos da tabela
    cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'vacinasbd' AND table_name = '{table_name}'")
    columns = cursor.fetchall()
    
    # Exibir os campos
    for column in columns:
        column_name, data_type = column
        print("- Campo:", column_name)
        print("  Tipo de Dado:", data_type)
    
    print()

# Fechar conexão
conn.close()