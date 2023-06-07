Aqui está o texto atualizado:

Projeto de Normalização de Dados e Análise de Aplicações de Vacina contra COVID-19

Este projeto é um exercício para treinar conhecimentos voltados para a área de engenharia de dados.

Este projeto tem como objetivo criar um banco de dados em um recurso do Azure MySQL Server, aplicando conceitos de normalização de dados, tipos de dados e constraints. Em seguida, serão populadas tabelas com os dados mais recentes sobre as aplicações de vacina contra COVID-19. Utilizaremos o armazenamento gratuito do Azure MySQL para armazenar essas informações.

Funcionalidades do Projeto

Criação do Banco de Dados: Será utilizado um script em Python para criar o banco de dados no recurso do Azure MySQL Server. O script incluirá a definição das tabelas, relacionamentos, tipos de dados e restrições necessárias para garantir a integridade dos dados.

Normalização de Dados: Serão aplicados princípios de normalização para organizar os dados em estruturas relacionais eficientes. Serão identificadas e eliminadas redundâncias, evitando anomalias e inconsistências.

População das Tabelas: Os dados necessários para popular as tabelas serão obtidos a partir das aplicações de vacina contra COVID-19 mais recentes. Faremos uso do script db_populate.py para processar e inserir os dados atualizados nas tabelas do banco de dados utilizando a biblioteca pandas.

Atualização Automática: Será criado um script no Azure Functions para atualizar o banco de dados com os dados mais recentes das aplicações de vacina contra COVID-19 diariamente às 23h59.

Análise de Dados: Após a população das tabelas, poderemos realizar análises exploratórias sobre os dados das aplicações de vacina contra COVID-19 mais recentes. Utilizaremos o Power BI para criar um dashboard interativo que apresentará informações relevantes, como estatísticas, gráficos e mapas geográficos.

Visualização dos Dados com Python: Além do Power BI, também exploraremos a criação de um dashboard similar utilizando Python em um Jupyter Notebook. Faremos uso de bibliotecas populares, como Pandas e Matplotlib, para realizar a visualização dos dados de maneira flexível e personalizada.

Requisitos e Dependências

Recurso do Azure MySQL Server: É necessário possuir um recurso do Azure MySQL Server para criar o banco de dados. As credenciais de acesso devem ser configuradas corretamente no script de criação do banco de dados.

Python 3.x: O projeto é desenvolvido em Python e requer a versão 3.x instalada no ambiente.

Bibliotecas Python: Será necessário instalar as seguintes bibliotecas Python:

pandas: Para a manipulação e análise dos dados.
matplotlib: Para a criação de gráficos e visualizações.
pyodbc: Para a conexão com o banco de dados MySQL.
Instruções de Uso
Clone este repositório em sua máquina local:

bash
Copy code
git clone https://github.com/matheustrevisan/vacinas_project_exercise.git
Configure as credenciais do Azure MySQL Server: No arquivo config.py, defina as informações de conexão com o recurso do Azure MySQL Server, como o nome do servidor, usuário e senha.

Execute o script de criação do banco de dados: Utilize o arquivo create_database.py para criar o banco de dados, tabelas e restrições no Azure MySQL Server.

Popule as tabelas com os dados mais recentes das aplicações de vacina contra COVID-19: Utilizando a biblioteca Spark, execute o script data_processing.py para processar e inserir os dados atualizados das aplicações de vacina nas tabelas do banco de dados.

Visualize os dados com o Power BI: Abra o arquivo dashboard.pbix no Power BI para explorar e visualizar os dados das aplicações de vacina contra COVID-19 em um dashboard interativo.

Próximos passos:
Visualize os dados com Python: Utilize o Jupyter Notebook fornecido (dashboard.ipynb) para executar o código Python e criar visualizações personalizadas dos dados das aplicações de vacina.

Contribuição e Suporte
Contribuições para este projeto são bem-vindas! Se você encontrar algum problema, tiver alguma ideia de melhoria ou quiser adicionar uma nova funcionalidade, sinta-se à vontade para abrir uma issue ou enviar um pull request.

Caso precise de suporte ou tenha alguma dúvida, por favor, entre em contato através dos meios listados abaixo.

Contato
Nome: Matheus Trevisan Facundo
Email: matheus.facundo@outlook.com
Website: https://www.linkedin.com/in/matheus-facundo/
