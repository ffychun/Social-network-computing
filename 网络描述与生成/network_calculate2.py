import networkx as nx
# import os
import powerlaw as pl
import csv
import matplotlib.pyplot as plt
from collections import Counter
import random

resultsPath = "C:\\Users\\范春\\Desktop\\results1.txt"

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

# 调用函数进行估计

def network_calculate(filePath,name):
    G = nx.Graph()
    with open(filePath,'r') as f:
        lines = f.readlines()
        # 这里得到的是迭代器！跳过第一行
        #next(reader)
        for line in lines[5:]:
            row = line.strip().split('\t')
            G.add_edge(int(row[0]),int(row[1]))
        print("读入数据完成"+name)
    '''
    with open(resultsPath , 'a') as result_file:
        print("结果文件打开啦")
        result_file.write(f"{name}:\n")
        result_file.write(f"顶点数:{len(G)}\n")
        result_file.write(f"边数:{G.size()}\n")
        result_file.write(f"密度:{nx.density(G)}\n")
        result_file.write(f"平均度:{2*G.size()/len(G)}\n")
        print("第一阶段完成")
    '''
        #try:
    print("最慢的计算开始啦")
            #average_L = nx.average_shortest_path_length(G)
            #result_file.write(f"平均最短路径 = {average_L}\n")
    estimated_avg_length = monte_carlo_shortest_path_length(G, num_samples=1000)
    print(f"Estimated average shortest path length: {estimated_avg_length}")
        #except nx.NetworkXError as e:
            #print(f"{e}\n")
        #result_file.write(f"网络的聚集系数1:{nx.average_clustering(G)}\n")
        #result_file.write(f"网络的聚集系数2:{nx.transitivity(G)}\n")
    '''
    print("要画图了")
    degrees = [G.degree(n) for n in G]
    fig,(ax1,ax2) = plt.subplots(1,2, figsize=(12, 6))

    degree_counts = Counter(degrees)
    total = sum(degree_counts.values())
    x,y = zip(*degree_counts.items())
    ax1.scatter(x, [c/total for c in y],color='green', s=15)
    ax1.set_title('Degree distribution')
    ax1.set_xlabel('k')
    ax1.set_ylabel('p(k)')

    pl.plot_pdf(degrees, color='blue',marker='o',ax=ax2)
    fit =pl.Fit(degrees,discrete=True) # 指定离散
    fit.power_law.plot_pdf(color='r',linestyle='--',ax=ax2,label=f'$\gamma={round(fit.power_law.alpha,2)}$, $p={round(fit.power_law.sigma,2)}$')
    with open(resultsPath , 'a') as result_file:
        result_file.write(f"powerlaw:\n")
        result_file.write(f"    gamma:{fit.power_law.alpha}\n")
        result_file.write(f"    p:{fit.power_law.sigma}\n")
        result_file.write("\n")
    ax2.set_title('Powerlaw distribution')
    ax2.set_xlabel('k')
    ax2.set_ylabel('p(k)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'C:\\Users\\范春\\Desktop\\{name}.png')'''
    print(f'{name} is ok!')

'''
filePaths = ["C:\\Users\\范春\\Desktop\\gemsec_deezer_dataset\\deezer_clean_data\\HR_edges.csv",
             "C:\\Users\\范春\\Desktop\\gemsec_deezer_dataset\\deezer_clean_data\\HU_edges.csv",
             "C:\\Users\\范春\\Desktop\\gemsec_deezer_dataset\\deezer_clean_data\\RO_edges.csv"]
names = ['HR_edges','HU_edges','RO_edges']
for i in range(3):
    print(i)
    network_calculate(filePaths[i],names[i])
'''
filePath="C:\\Users\\范春\\Desktop\\week2\\as-skitter.txt\\as-skitter.txt"
name = "as-skitter"
network_calculate(filePath, name)