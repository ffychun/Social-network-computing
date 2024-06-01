import networkx as nx
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import copy

def generateNet(filePath):
    # 读取数据并创建图
    df = pd.read_csv(filePath)
    G = nx.Graph()
    for index, row in df.iterrows():
        G.add_edge(int(row['node_1']), int(row['node_2']))

    # 选择一个随机的初始节点
    initial_node = random.choice(list(G.nodes))
    
    # 执行随机游走直到子图包含1000个节点
    visited = set([initial_node])
    current_node = initial_node
    while len(visited) < 100:
        neighbors = list(G.neighbors(current_node))
        if not neighbors:
            break
        current_node = random.choice(neighbors)
        visited.add(current_node)
    
    # 创建子图
    subgraph = G.subgraph(visited)
    return subgraph

# 代理类  
class Agent:  
    def __init__(self, memory_length):
        self.memory_length = memory_length  
        self.memory = ['A'] * memory_length  
  
    def update_memory(self, info):  
        self.memory.pop(0)  
        self.memory.append(info) 

    def update_allmemory(self,info):
        self.memory = [info]*self.memory_length
  
    def get_most_common_info(self):  
        return max(set(self.memory), key=self.memory.count) 
    
    def check_B_majority(self):  
        count_B = self.memory.count('B')  
        half_length = len(self.memory) /2  
        if count_B > half_length:  
            return 1  
        else:  
            return 0
    
def simulate(G):
    results = {}
    for M in range(1,21):
        print('M: ',M)
        agents = {node: Agent(M) for node in G.nodes()}
        for C in np.arange(0.1,0.61,0.01):
            print('C: ',C)
            total_B_majority = 0
            agents_copy = copy.deepcopy(agents)
            minority_agents = random.sample(list(agents_copy.keys()), int(C*100))

            for node in minority_agents:
                agents_copy[node].update_allmemory('B')

            for T in range(100):
                for N in range(100):
                    selected_edge = random.choice(list(G.edges()))
                    speaker, hearer = random.sample(selected_edge, 2)
                    
                    if hearer not in minority_agents:
                        if speaker in minority_agents:
                            agents_copy[hearer].update_memory('B')
                        else:
                            agents_copy[hearer].update_memory(agents_copy[speaker].get_most_common_info())

            total_B_majority += sum(agents_copy[node].check_B_majority() for node in agents_copy)-C*100
            print(total_B_majority)
            if total_B_majority/(100-C*100)>=0.9:
                results[M]=C
                print("M  C: ", M, C)
                break
    return results

def main():
    filePath = "C:\\Users\\范春\\Desktop\\week8\\gemsec_deezer_dataset\\deezer_clean_data\\HR_edges.csv"
    G = generateNet(filePath)
    print(len(G))
    print(len(G.edges()))
    print("网络生成成功")
    results = simulate(G)
    M = list(results.keys())
    tipping_point = list(results.values())

    plt.plot(M, tipping_point, marker='o')
    plt.show()
    df = pd.DataFrame({'M':M,'tipping_point':tipping_point})
    df.to_excel("C:\\Users\\范春\\Desktop\\week8\\results.xlsx",index=False)

if __name__=='__main__':
    main()




