import mysql.connector
import config

# Conectar ao banco de dados
conn = mysql.connector.connect(
    user=config.user,
    password=config.password,
    host=config.host
)

# Criar cursor para executar comandos SQL
cursor = conn.cursor()

# Criar o banco de dados "vacinasbd"
cursor.execute("CREATE DATABASE IF NOT EXISTS vacinasbd")

conn.database = 'vacinasbd'

# Criar tabela Paises
cursor.execute(
'''
    CREATE TABLE Paises (
        coPais VARCHAR(10) PRIMARY KEY NOT NULL,
        nmPais VARCHAR(45)
    )
''')

# Criar tabela RacaCor
cursor.execute(
'''
    CREATE TABLE RacaCor (
        raca_cor_codigo ENUM('1', '2', '3', '4', '99') PRIMARY KEY NOT NULL,
		raca_cor_valor VARCHAR(45)
    )
''')

# Criar tabela Municipio
cursor.execute(
'''
    CREATE TABLE Municipio (
        municipio_codigo VARCHAR(10) PRIMARY KEY NOT NULL,
        municipio_nome VARCHAR(100),
        uf_sigla CHAR(2) NOT NULL,
        coPais VARCHAR(10),
        FOREIGN KEY (coPais) REFERENCES Paises(coPais)
    )
''')

# Criar tabela Estabelecimento
cursor.execute(
'''
    CREATE TABLE Estabelecimento (
        estabelecimento_valor VARCHAR(10) PRIMARY KEY NOT NULL,
        estabelecimento_razaoSocial VARCHAR(100),
        estabelecimento_noFantasia VARCHAR(100),
        estabelecimento_municipio_codigo VARCHAR(10),
        FOREIGN KEY (estabelecimento_municipio_codigo) REFERENCES Municipio(municipio_codigo)
    )
''')

# Criar tabela VacinaGrupoAtendimento
cursor.execute(
'''
    CREATE TABLE VacinaGrupoAtendimento (
        vacina_grupo_atendimento_code VARCHAR(10) PRIMARY KEY NOT NULL,
        vacina_grupo_atendimento_nome VARCHAR(255)
    )
''')

# Criar tabela CategoriaVacina
cursor.execute(
'''
    CREATE TABLE CategoriaVacina (
        vacina_categoria_code VARCHAR(10) PRIMARY KEY NOT NULL,
        vacina_categoria_nome VARCHAR(100)
    )
''')

# Criar tabela FabricanteVacina
cursor.execute(
'''
    CREATE TABLE FabricanteVacina (
        vacina_fabricante_referencia VARCHAR(45) PRIMARY KEY NOT NULL,
        vacina_fabricante_nome VARCHAR(45)
    )
''')

# Criar tabela Vacina
cursor.execute(
'''
    CREATE TABLE Vacina (
        vacina_codigo VARCHAR(45) PRIMARY KEY NOT NULL,
        vacina_lote VARCHAR(45),
        vacina_fabricante_referencia VARCHAR(45),
        vacina_grupo_atendimento_code VARCHAR(10) NOT NULL,
        vacina_categoria_code VARCHAR(10) NOT NULL,
        FOREIGN KEY (vacina_fabricante_referencia) REFERENCES FabricanteVacina(vacina_fabricante_referencia),
        FOREIGN KEY (vacina_grupo_atendimento_code) REFERENCES VacinaGrupoAtendimento(vacina_grupo_atendimento_code),
        FOREIGN KEY (vacina_categoria_code) REFERENCES CategoriaVacina(vacina_categoria_code)
    )
''')

# Criar tabela Paciente
cursor.execute(
'''
    CREATE TABLE Paciente (
        paciente_id VARCHAR(100) PRIMARY KEY NOT NULL,
        paciente_data_nascimento DATE,
        paciente_enumSexoBiologico ENUM('M', 'F'),
        paciente_racaCor_codigo ENUM('1', '2', '3', '4', '99'),
        paciente_endereco_colbgeMunicipio VARCHAR(10),
        paciente_endereco_cep VARCHAR(8),
        paciente_nacionalidade_enumNacionalidade VARCHAR(10),
        FOREIGN KEY (paciente_racaCor_codigo) REFERENCES RacaCor(raca_cor_codigo),
        FOREIGN KEY (paciente_endereco_colbgeMunicipio) REFERENCES Municipio(municipio_codigo)
    )
''')

# Criar tabela Aplicacoes
cursor.execute(
'''
    CREATE TABLE Aplicacoes (
        aplicacao_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        paciente_id VARCHAR(100) NOT NULL,
        estabelecimento_valor VARCHAR(10) NOT NULL,
        vacina_codigo VARCHAR(45) NOT NULL,
        sistema_origem VARCHAR(100),
        vacina_data_aplicacao DATETIME,
        vacina_descricao_dose VARCHAR(100),
        document_id VARCHAR(100) NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES Paciente(paciente_id),
        FOREIGN KEY (estabelecimento_valor) REFERENCES Estabelecimento(estabelecimento_valor),
        FOREIGN KEY (vacina_codigo) REFERENCES Vacina(vacina_codigo)
    )
''')

# Commit das alterações e fechar conexão
conn.commit()
conn.close()
