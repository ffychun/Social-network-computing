import networkx as nx
import numpy as np
import itertools
import random
import pandas as pd

# 创建BA网络  
def create_ba_network(n, m):  
    # n: 网络中节点数量  
    # m: 附加到每个新节点的现有节点数量  
    return nx.barabasi_albert_graph(n, m)  

#优先附着
def preferential_attachment_path(G, source, target,degrees,alpha):  
    # 初始化路径  
    path = [source]  
    current_node = source  
    while current_node != target:  
        # 获取当前节点的邻居  
        neighbors = list(G.neighbors(current_node))  

        # 过滤掉已经访问过的邻居  
        neighbors = [node for node in neighbors if node not in path]
          
        # 如果没有邻居或所有邻居都已经检查过则退出循环
        if len(neighbors) == 0:  
            break   
       
        # 如果邻居中包含目标节点，则直接返回路径  
        elif target in neighbors:  
            path.append(target)  
            return path  
          
        # 否则随机选取一个邻居作为下一个节点  
        else:
            # 计算每个邻居节点被选中的概率（度数占比）  
            degree = [degrees[node]**alpha for node in neighbors]  
            total_degree = sum(degree)  
            probabilities = [deg / total_degree for deg in degree]  

            pa_node = np.random.choice(neighbors, p=probabilities) 
            path.append(pa_node)  
            current_node = pa_node
    return path

# 估计平均路径长度  
def estimate_average_path_length(G, alpha):  
    # 随机获取一千个节点对  
    node_pairs = random.sample(list(itertools.combinations(G.nodes(), 2)),1000)
    degrees = dict(G.degree())

    # 初始化路径长度列表  
    path_lengths = []  
    
    # 遍历所有节点对  
    for source, target in node_pairs:  
        path = preferential_attachment_path(G, source, target,degrees, alpha)  
        path_lengths.append(len(path) - 1)  
      
    # 计算平均路径长度  
    average_path_length = np.mean(path_lengths)
    return average_path_length

def main():
    m = 3
    n = 5000
    G = create_ba_network(n,m)
    results = []
    for item in np.arange(0,10.25,0.5):
        print(item)
        average_path_length = estimate_average_path_length(G, item)
        results.append((item, average_path_length))  
      
    df = pd.DataFrame(results, columns=['item', 'average_path_length'])  
       
    df.to_excel("C:\\Users\\范春\\Desktop\\week7\\results2.xlsx", index=False) 

if __name__=="__main__":
    main()
