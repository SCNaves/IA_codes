import networkx as nx
import matplotlib.pyplot as plt

# Função criada para percorrer as cidades e verificar o menor custo
def cost_function(initial_city, destiny_city, List_of_nodes, qtde_cities):
    
    # Vetor para salvar as cidades visitadas ao longo do código
    cities_visited = [0] * qtde_cities  # Cria um vetor de cidades visitadas
    cities_visited[0] = str(initial_city)   # A cidade inicial é o primeiro index do vetor

    # O vetor 'cost_city' é responsável por conter os nós adjacentes ao atual nó em estudo
    # É por ele que será decidido qual o nó seguinte de menor custo
    cost_city = []
    cost_city.append((initial_city,0)) #Insere a cidade inicial com custo zero 

    # Vetor para conter a cidade atual (inicialmente é composto pela cidade inicial, porém ao longo do código
    # será composto pela cidade de menor custo). 
    actual_city = []
    actual_city = initial_city
    
    i = 1   # Iniciando variável para guardar o numero de cidades que foram visitadas ao final do algoritmo (inicia com 1 porque a cidade inicial já deve ser contada)
    while True:

        # Caso a cidade atual seja igual a cidade de destino sair do loop
        if actual_city == destiny_city:
            print("Chegamos a sua cidade destino: ", actual_city)
            print("As cidades visitadas pelo caminho foram: ")
            # Como o vetor 'cities_visited' pode não conter todos os campos compostos por cidade, será retirado apenas os indíces
            # que que possuem strings como forma
            for i, city in enumerate(cities_visited):   #Comando enumerate retorna a posição e a palavra contida no vetor nesta posição. Ex: '0' 'Goiana'
                if isinstance(city,str):    #Caso a palavra seja de formato string, printar na tela
                    print(city)
            break
        
        city_vec = []   # Vetor para guardar as possíveis cidades a serem visitadas
        cost_vec = []   # Vetor para conter os custos das possíveis cidades e determinar o menor entre eles 
        for city, cost in List_of_nodes[actual_city]:
           city_vec.append(city)
           cost_vec.append(cost) 
           
        # Excluir as cidades já visitadas do vetor city_vec
        city_vec = [city for city in city_vec if city not in cities_visited]
        """
        # Removendo a cidade atual para que ela não seja uma próxima opção ao longo do algoritmo
        if i > 1:
            if cities_visited in city_vec:
                idx = city_vec.index(cities_visited)   # Pegando o index correspondente a cidade atual
                city_vec.remove(cities_visited)    # Eliminando a cidade do vetor de opções
                cost_vec.pop(idx)    # Eliminando o custo do vetor de opções
        """
        # Aqui é retirado o index associado ao menor custo contido no vetor 'cost_vec'. 
        # Dessa maneira, é possível referenciar o index a 'city_vec' e determinar a cidade associada ao index de menor custo
        lower_cost_idx = cost_vec.index(min(cost_vec))  # index de menor custo
        actual_city = city_vec[lower_cost_idx]  # Aloca a cidade associada ao index de menor custo ao vetor 'actual_city' esta sera agora a próxima cidade a ser analisada

        # Guarda a cidade de menor custo no vetor criado anteriormente (irá conter todas as cidades visitadas)
        cities_visited[i] = actual_city

        # Atualiza o valor da variável
        i = i + 1

    return cities_visited

# Criando um vetor da quantidade de cidades a serem utilizados no código
qtde_cities = 12

# Vetor para conter cidades ja visitadas (possui um tamanho inicial do n° de cidades existentes)
visited_cities = [[] for i in range(qtde_cities)] # Vetor vazio do tamanho do vetor "qtde_cities"

# Criando uma lista para conter todos os nós e seus respectivos vizinhos juntamente ao valor de custo
"""
Exemplo: Lista_de_nos = {
                    Cidade: [Cidade vizinha, custo associado]
}
"""

List_of_nodes = {
    'Sao Paulo': [('Campinas',1),('Rio de Janeiro',3),('Curitiba',4),('Joinville',5),('Belo Horizonte',9)],
    'Campinas': [('Sao Paulo',1),('Curitiba',5),('Belo Horizonte',8),('Uberlandia',12)],
    'Uberlandia': [('Belo Horizonte',5),('Goiana',7),('Brasilia',9),('Campinas',12),('Curitiba',18)],
    'Goiana': [('Brasilia',2),('Uberlandia',7),('Florianopolis',20)],
    'Brasilia': [('Goiana',2),('Uberlandia',9),('Salvador',20)],
    'Salvador': [('Ilheus',4),('Belo Horizonte',16),('Brasilia',20)],
    'Ilheus': [('Salvador',4),('Rio de Janeiro',6),('Belo Horizonte',10)],
    'Belo Horizonte': [('Uberlandia',5),('Rio de Janeiro',7),('Campinas',8),('Sao Paulo',9),('Ilheus',10),('Salvador',16)],
    'Rio de Janeiro': [('Sao Paulo',3),('Ilheus',6),('Belo Horizonte',7),('Joinville',15)],
    'Joinville': [('Curitiba',2),('Sao Paulo',5),('Florianopolis',5),('Rio de Janeiro',15)],
    'Curitiba': [('Joinville',2),('Florianopolis',4),('Sao Paulo',4),('Campinas',5),('Uberlandia',18)],
    'Florianopolis': [('Curitiba',4),('Joinville',5),('Goiana',20)]
} 

#PLOT GRAFOS

# Criando um grafo utilizando da biblioteca 'networkx'
G = nx.Graph()

# Adicionando as cidades contidas nas listas para o grafo
for city in List_of_nodes.keys():   # 'keys()' é utilizada para retirar as primeiras cidades associadas ao dicionário em 'List_of_nodes'
    G.add_node(city)

for city, cost in List_of_nodes.items():    # 'items()' é utilizado para retirar os valores associados a cada cidade no dicionário
    for connection in cost:
        G.add_edge(city,connection[0])

# Plotar o grafo
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

# Recebendo os parâmetros do usuário
print("Digite a cidade de partida: ")
initial_city = input()
print("Digite a cidade de destino: ")
destiny_city = input()

cidades_visitadas = cost_function(initial_city, destiny_city, List_of_nodes, qtde_cities)
