import pandas as pd
from mysql.connector import connect, Error
from config import user, password, host, database

import mysql.connector

# Configurações de conexão ao banco de dados
config = {
    'user': user,
    'password': password,
    'host': host,
    'database': database
}

# Função para obter o número de registros de cada tabela
def count_records():
    try:
        # Conectando ao banco de dados
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Obtendo a lista de tabelas
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Iterando sobre as tabelas e obtendo o número de registros
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"A tabela '{table_name}' possui {count} registros.")

    except mysql.connector.Error as e:
        print(f"Erro ao acessar o banco de dados: {e}")

    finally:
        # Fechando a conexão
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# Chamando a função para contar os registros
count_records()
