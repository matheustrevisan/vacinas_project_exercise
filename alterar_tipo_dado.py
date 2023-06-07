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

# Desabilitar a verificação de chaves estrangeiras temporariamente

cursor.execute("SET FOREIGN_KEY_CHECKS=0")

# Alterar o tipo de dado do campo paciente_id na tabela Paciente
#alter_query = "ALTER TABLE Paciente MODIFY paciente_id VARCHAR(100)"
#cursor.execute(alter_query)

# Executar uma operação que viola a integridade referencial
cursor.execute("INSERT INTO Aplicacoes (paciente_id,estabelecimento_valor) VALUES (999,999)")

# Alterar o tipo de dado do campo paciente_id na tabela Aplicacoes
alter_aplicacoes_query = "ALTER TABLE Aplicacoes MODIFY paciente_id VARCHAR(100)"
cursor.execute(alter_aplicacoes_query)

# Habilitar a verificação de chaves estrangeiras novamente
cursor.execute("SET FOREIGN_KEY_CHECKS=1")

# Commit das alterações e fechar conexão
conn.commit()
conn.close()
