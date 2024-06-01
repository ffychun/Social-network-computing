import networkx as nx  
import numpy as np  
import random 
from multiprocessing import Pool
import pandas as pd
import matplotlib.pyplot as plt

# 创建二维格子网络并添加长程边  
def create_grid_with_long_range_edges(N, p):  
    # 创建N*N的二维格子网络  
    G = nx.grid_2d_graph(N, N, periodic=False)  
      
    # 添加长程边  
    n = N*N
    num_long_range_edges = int(p * (n*(n-1)/2))  # 假设p是相对于总节点数的比例  
    existing_edges = set(G.edges())  
    nodes = list(G.nodes())
      
    while num_long_range_edges > 0:  
        # 随机选择两个不同的节点  
        node1, node2 = random.sample(nodes, 2)  
        # 如果这对节点之间没有边并且不是自环，则添加边  
        if (node1, node2) not in existing_edges and node1 != node2:  
            G.add_edge(node1, node2)  
            existing_edges.add((node1, node2))  
            num_long_range_edges -= 1  

    states = np.array([1] * (n // 2) + [-1] * (n // 2)) 
    np.random.shuffle(states)
    state_dict = dict(zip(nodes, states))
    nx.set_node_attributes(G, state_dict, 'state')

    return G, existing_edges

# Voter模型模拟函数  
def voter_model_simulation(G, T, existing_edges):  
    results = []
    nodes = list(G.nodes())
    # 获取节点位置
    pos = {node: (node[0], node[1]) for node in G.nodes()}
   
    for i in range(T):  
        print(i)
        if (i==10000 or i==20000 or i==30000):
        #可视化
            visualize_opinion_distribution(G, pos, i)

        # 随机选择一个节点  
        node = random.sample(nodes, 1)[0]
        #print(node)
        # 随机选择一个邻居  
        neighbors = list(G.neighbors(node))
        if neighbors:
            neighbor = random.sample(neighbors, 1)[0]  
            #print(neighbor)
            # 更新节点状态  
            G.nodes[node]['state'] = G.nodes[neighbor]['state']
            results.append(calculate_na(G, existing_edges))
    
    return results

def calculate_na(G, existing_edges):
    result = 0
    for edges in existing_edges:
        node1 = edges[0]
        node2 = edges[1]
        if G.nodes[node1]['state'] != G.nodes[node2]['state']:
            result+=1
    
    return result/len(existing_edges)

def run(N, p):
    G, existing_edges = create_grid_with_long_range_edges(N, p)
    results = voter_model_simulation(G,1000000,existing_edges)

    return results


def visualize_opinion_distribution(G, pos, t):
    # 根据节点状态分组
    positive_nodes = [node for node, data in G.nodes(data=True) if data['state'] == 1]
    negative_nodes = [node for node, data in G.nodes(data=True) if data['state'] == -1]

    #print(len(positive_nodes))
    #print(len(negative_nodes))
    # 绘制正观点的节点
    nx.draw_networkx_nodes(G, pos, nodelist=positive_nodes, node_color='blue', label='Positive Opinion')
    # 绘制负观点的节点
    nx.draw_networkx_nodes(G, pos, nodelist=negative_nodes, node_color='red', label='Negative Opinion')

    # 设置图例
    #plt.legend()
    # 设置标题
    #plt.title('Opinion Distribution')
    figPath = f"C:\\Users\\范春\\Desktop\\week10\\img\\{t}.png"
    plt.savefig(figPath)


def main():
    N = 10
    p_values=[0.01,0.05,0.03]

    run(30,0.05)
    

if __name__=='__main__':
    main()
  
