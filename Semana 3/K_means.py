import pandas as pd               # for Data Manipulation
import matplotlib.pyplot as plt   # for Visualization
import numpy as np                #for Mathematical calculations
import seaborn as sns             #for Advanced visualizations
from scipy.stats.mstats import winsorize
from sklearn import preprocessing
from sklearn.cluster import KMeans

"""
ID# --Unique ID

Balance--Number of miles eligible for award travel

Qual_mile--Number of miles counted as qualifying for Topflight status

cc1_miles -- Number of miles earned with freq. flyer credit card in the past 12 months:

cc2_miles -- Number of miles earned with Rewards credit card in the past 12 months:

cc3_miles -- Number of miles earned with Small Business credit card in the past 12 months:

1 = under 5,000

2 = 5,000 - 10,000

3 = 10,001 - 25,000

4 = 25,001 - 50,000

5 = over 50,000

Bonus_miles--Number of miles earned from non-flight bonus transactions in the past 12 months

Bonus_trans--Number of non-flight bonus transactions in the past 12 months

Flight_miles_12mo--Number of flight miles in the past 12 months

Flight_trans_12--Number of flight transactions in the past 12 months

Days_since_enrolled--Number of days since enrolled in flier program

Award?--whether that person had award flight (free flight) or not

# As a part of
"""

def tratamentoOutliers(air):
# Retirando os OUTLIERS do banco de dados
# Temos sempre na estatística o intervalo de confiança (IC) dos nossos dados
# Deste modo, será realizado abaixo a exclusão dos OUTLIERS através do comando winsorize da biblioteca scipy
# onde todo valor abaixo do percentil 5 será substítuido pelo valor do percentil 5
# e todo valor acima do percentil 95 será substituído pelo valor do percentil 95

    # Limites para a winsorização
    limits = [0.05, 0.095]

    # Lista das colunas a serem tratadas
    columns = air.columns
    columns = columns.drop(['ID'], ['Award'])
    for column in columns:
        air[column] = winsorize(air[column], limits=limits)

"""
INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO
INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO
INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO // INÍCIO DO CÓDIGO
"""

# Trazendo o dataset
air = pd.read_csv("EastWestAirlines.csv")

# Chamando a função de tratamento dos dados: Outliers
tratamentoOutliers(air)

# Verificar se existem campos nulos no nosso dataset e exclui a respectiva coluna
print((air == 0).all())
air1 = air
#air1.drop(["Qual_miles", "Bonus_miles", "Days_since_enroll"], axis=1,inplace = True)
air1.drop(["Qual_miles"], axis=1,inplace = True)

# Normalizando o dataset
air_normalized = preprocessing.normalize(air1)

# MÉTODO K-MEANS
TWSS = []
k = list(range(2, 100))  # Variando k entre uma faixa de valores para verificar o mais adequado

for i in k:
    kmeans = KMeans(n_clusters = i).fit(air_normalized) # Fit dos dados do dataset
    TWSS.append(kmeans.inertia_)    # Salvando a 'Soma dos Quadrados' entre os pontos e o cluster principal de cada iteração
    #print(TWSS)
    print("O menor erro quadrático é: k = {}: {}".format(i, np.min(TWSS)))

print("O valor mínimo do SSE é: {}".format(np.min(TWSS)))
print("O valor médio do SSE é:{}", np.mean(TWSS))

# Plotando a convergência do modelo X número de Clusters
plt.plot(k, TWSS, 'ro-')
plt.title("SSE")
plt.xlabel("Número de Clusters")
plt.ylabel("Distancia (Soma dos Quadrados)")
plt.show()

# Verificando qual o melhor valor de k a ser escolhido

# Plotar os dados divididos em clusters
fig, axs = plt.subplots(2, 2, figsize=(10, 10))
axs = axs.flatten()

k_values = [24,25,26,27]
labels = []
for i, k in enumerate(k_values):
    # Chamando k-means de acordo com o valor de k desejado
    model = KMeans(n_clusters = k).fit(air_normalized)  # Fit dos dados 
    labels.append(model.labels_)  # Rótulo dado pelo 'K-Means' para cada um dos passageiros

    # Convertendo numpy array em pandas object 
    mb = pd.Series(model.labels_)  

    # Trazendo o DataSet original
    air1 = pd.read_csv("EastWestAirlines.csv")
    air1['cluster'] = mb # Criando uma nova coluna 'cluster' e adicionando os rótulos a ela

    # Fazendo de 'cluster' a coluna primária e depois o dataset segue como original
    air = air1.iloc[:,[12,0,1,2,3,4,5,6,7,8,9,10,11]]

    # Agrupando os usuários de acordo com seus rótulos, ou seja, usuários que se assemelham fazem parte de um mesmo cluster
    air.iloc[:, 1:12].groupby(air.cluster).mean()     

    # Salvar 'air_means' em um arquivo Excel com o valor de k no nome do arquivo
    air.to_excel(f'resultado_clusters_k{k}.xlsx', index=False)

for i, label in enumerate(labels):
    axs[i].scatter(air_normalized[:, 0], air_normalized[:, 1], c=label, cmap='viridis')
    axs[i].set_title(f'Clusters para k={k_values[i]}')

plt.tight_layout()
plt.show()