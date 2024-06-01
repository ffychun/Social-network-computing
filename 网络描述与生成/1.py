import networkx as nx
# import os
import powerlaw as pl
import csv
import matplotlib.pyplot as plt
from collections import Counter
import random

def monte_carlo_shortest_path_length(G, num_samples=1000):
    total_length = 0
    count = 0
    for _ in range(num_samples):
        node1, node2 = random.sample(list(G.nodes), 2)
        try:
            length = nx.shortest_path_length(G, node1, node2)
            total_length += length
            count += 1
        except nx.NetworkXNoPath:
            continue
    avg_length = total_length / count if count > 0 else 0
    return avg_length
def network_calculate(filePath,name):
    G = nx.Graph()
    with open(filePath,'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            G.add_edge(int(row[0]),int(row[1]))

    estimated_avg_length = monte_carlo_shortest_path_length(G, num_samples=1000)
    print(f"Estimated average shortest path length: {estimated_avg_length}")
    '''
    with open(resultsPath , 'a') as result_file:
        result_file.write(f"{name}:\n")
        result_file.write(f"vertexes number:{len(G)}\n")
        result_file.write(f"edges number:{G.size()}\n")
        result_file.write(f"density:{nx.density(G)}\n")
        result_file.write(f"average degree:{2*G.size()/len(G)}\n")
        try:
            average_L = nx.average_shortest_path_length(G)
            result_file.write(f"L = {average_L}\n")
        except nx.NetworkXError as e:
            result_file.write(f"{e}\n")
        result_file.write(f"clustering1:{nx.average_clustering(G)}\n")
        result_file.write(f"clustering2:{nx.transitivity(G)}\n")
    
    degrees = [G.degree(n) for n in G]
    fig,(ax1,ax2) = plt.subplots(1,2, figsize=(12, 6))

    degree_counts = Counter(degrees)
    total = sum(degree_counts.values())
    x,y = zip(*degree_counts.items())
    ax1.scatter(x, [c/total for c in y],color='b', s=15)
    ax1.set_title('degree distribution')
    ax1.set_xlabel('k')
    ax1.set_ylabel('p(k)')

    pl.plot_pdf(degrees, color='b',marker='o',ax=ax2)
    fit =pl.Fit(degrees,discrete=True) # 指定离散
    fit.power_law.plot_pdf(color='r',linestyle='--',ax=ax2,label=f'$\gamma={round(fit.power_law.alpha,2)}$, $p={round(fit.power_law.sigma,2)}$')
    with open(resultsPath , 'a') as result_file:
        result_file.write(f"powerlaw:\n")
        result_file.write(f"    gamma:{fit.power_law.alpha}\n")
        result_file.write(f"    p:{fit.power_law.sigma}\n")
        result_file.write("\n")
    ax2.set_title('powerlaw distribution')
    ax2.set_xlabel('k')
    ax2.set_ylabel('p(k)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'E:\\c盘\\桌面\\大三学习\\复杂网络与社会计算\\week2\\results\\figures\\{name}.png')'''
    print(f'{name} is ok!')


filePaths = ["C:\\Users\\范春\\Desktop\\week2\\gemsec_deezer_dataset\\deezer_clean_data\\HR_edges.csv",
             "C:\\Users\\范春\\Desktop\\week2\\gemsec_deezer_dataset\\deezer_clean_data\\RO_edges.csv",
             "C:\\Users\\范春\\Desktop\\week2\\gemsec_deezer_dataset\\deezer_clean_data\\HU_edges.csv"]
names = ['HR_edges','RO_edges','HU_edges']
for i in range(3):
    network_calculate(filePaths[i],names[i])