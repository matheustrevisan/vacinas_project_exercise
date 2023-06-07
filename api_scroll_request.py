import requests
import sys

url = "https://imunizacao-es.saude.gov.br/_search?scroll=1m"
credentials = ("imunizacao_public", "qlto5t&7r_@+#Tlstigi")
headers = {
    "Content-Type": "application/json",
}

body = {
    "size": 10000
}

all_hits = []  # Variável para armazenar todos os hits
max_memory = 5 * 1024 * 1024 * 1024  # 5GB em bytes

# Fazendo a primeira requisição
response = requests.get(url, auth=credentials, headers=headers, json=body)
data = response.json()

# Processando os hits da primeira requisição
hits = data.get("hits", {}).get("hits", [])
all_hits.extend(hits)

# Obtendo o valor inicial do scroll_id
scroll_id = data.get("_scroll_id", "")

# Realizando as requisições subsequentes até que a lista de hits esteja vazia ou o limite de memória seja atingido
while len(hits) > 0 and sys.getsizeof(all_hits) + sys.getsizeof(hits) < max_memory:
    params = {
        "scroll_id": scroll_id,
        "scroll": "1m"
    }

    # Fazendo a requisição seguinte
    response = requests.get(url, auth=credentials, headers=headers, params=params)
    data = response.json()

    # Processando os hits da requisição seguinte
    hits = data.get("hits", {}).get("hits", [])
    
    # Verificando se o tamanho total não excede o limite de memória
    if sys.getsizeof(all_hits) + sys.getsizeof(hits) < max_memory:
        all_hits.extend(hits)
    else:
        break

    # Atualizando o valor do scroll_id para a próxima requisição
    scroll_id = data.get("_scroll_id", "")

# Exibindo os resultados
for hit in all_hits:
    print(hit)
