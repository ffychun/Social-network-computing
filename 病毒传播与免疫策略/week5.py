import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import EoN
import numpy as np
import random

#生成网络
def network(filePath):
    G = nx.Graph()

    df = pd.read_excel(filePath)
    columns = df.columns
    for index, row in df.iterrows():
        col1_value = row[columns[0]]
        col2_value = row[columns[1]]
        G.add_edge(int(col1_value),int(col2_value))

    return G

#分析网络的rich_club特征
def rich_club(G):
    rc = nx.rich_club_coefficient(G, normalized=True, Q=1)
    
    with open('C:\\Users\\范春\\Desktop\\week5\\rich_club_coefficient.pkl', 'wb') as f:
        pickle.dump(rc, f)



#分析网络的度-度相关性    
def degree_degree(G):
    avg_neighbor_degrees = nx.average_neighbor_degree(G)
    r = nx.degree_assortativity_coefficient(G)

    degrees_to_avg_neighbors = {}
    for node, degree in G.degree():
        if degree in avg_neighbor_degrees:
            if degree not in degrees_to_avg_neighbors:
                degrees_to_avg_neighbors[degree] = []
            for neighbor in G.neighbors(node):
                if G.degree(neighbor) in avg_neighbor_degrees:
                    degrees_to_avg_neighbors[degree].append(avg_neighbor_degrees[G.degree(neighbor)])

    with open('C:\\Users\\范春\\Desktop\\week5\\avg_neighbor_degrees.pkl', 'wb') as f:
        pickle.dump(degrees_to_avg_neighbors, f)

    return r


def SIS_SIR(G):
    tau = [0.2,0.25,0.3,0.35]
    gamma = [0.15,0.2,0.25,0.3]

    for i in range(4):
        t, S, I = EoN.fast_SIS(G, tau[i], gamma[i],tmax=50, initial_infecteds=range(5))
        filename = f"C:\\Users\\范春\\Desktop\\week5\\SIS_tau_{tau[i]}_gamma_{gamma[i]}.csv"
        np.savetxt(filename,np.column_stack((t,S,I)),delimiter=',',header='t,S,I')
    print("SIS完成")
    for i in range(4):
        t, S, I, R = EoN.fast_SIR(G,tau[i],gamma[i], initial_infecteds=range(5))
        filename = f"C:\\Users\\范春\\Desktop\\week5\\SIR_tau{tau[i]}_gamma_{gamma[i]}.csv"
        np.savetxt(filename,np.column_stack((t,S,I,R)),delimiter=',',header='t,S,I,R')

def question4(G):
    # 初始化免疫比例列表和对应的感染比例变化列表  
    immunization_fractions = np.linspace(0, 0.9, 10)
    infection_ratio_changes = {'random': [], 'target': []} 

    tau = 0.25
    gamma = 0.2

    G_copy = G.copy()
    t1, S1, I1 = EoN.fast_SIS(G_copy, tau, gamma,tmax=50, initial_infecteds=range(5))

    for immunization_fraction in immunization_fractions:
        print(immunization_fraction) 

        # 随机策略  
        G_random = G.copy()  
        random_nodes = random.sample(list(G_random.nodes()), int(G.number_of_nodes() * immunization_fraction)) 
        print(G.number_of_nodes()) 
        print(len(random_nodes))
        #print(random_nodes)
        random_nodes = [node for node in random_nodes if node in G_random.nodes()]
        G_random.remove_nodes_from(random_nodes)
        t2, S2, I2 = EoN.fast_SIS(G_random, tau, gamma,tmax=50, initial_infecteds=range(5))  
        p1 = np.mean(I2) / np.mean(I1)
        print("p1: ",p1)
        infection_ratio_changes['random'].append(p1)


        # 目标策略  
        G_target = G.copy()  
        node_degrees = dict(G.degree())
        sorted_nodes = sorted(node_degrees, key=lambda x:node_degrees[x],reverse=True)
        target_nodes = sorted_nodes[:int(G.number_of_nodes() * immunization_fraction)]
        target_nodes = [node for node in target_nodes if node in G_target.nodes()]
        G_target.remove_nodes_from(target_nodes)  
        t3, S3, I3 = EoN.fast_SIS(G_target, tau, gamma, tmax=50, initial_infecteds=range(5))  
        p2 = np.mean(I3) / np.mean(I1)
        print("p2: ",p2)
        infection_ratio_changes['target'].append(p2)

        # 熟人策略  
        '''G_acquaintance = G.copy()  
        acquaintance_nodes = []  
        for _ in range(int(G.number_of_nodes() * immunization_fraction)):  
            random_node = np.random.choice(G_acquaintance.nodes())  
            acquaintance_nodes.append(np.random.choice(list(G_acquaintance.neighbors(random_node))))  
        acquaintance_nodes = [node for node, degree in acquaintance_nodes if node in G_acquaintance.nodes()]
        G_acquaintance.remove_nodes_from(set(acquaintance_nodes))  
        t4, S4, I4 = EoN.fast_SIS(G_acquaintance, tau, gamma, tmax = 50,initial_infecteds=range(5))  
        p3 = np.mean(I4) / np.mean(I1)
        print("p3: ",p3)
        infection_ratio_changes['acquaintance'].append(p3)'''  
    
    # 保存infection_ratio_changes到文件
    with open('C:\\Users\\范春\\Desktop\\week5\\infection_ratio_changes.pkl', 'wb') as f:
        pickle.dump(infection_ratio_changes, f)

    plt.figure(figsize=(10, 6))  
    plt.plot(immunization_fractions, infection_ratio_changes['random'], label='Random Strategy')  
    plt.plot(immunization_fractions, infection_ratio_changes['target'], label='Target Strategy')  
    #plt.plot(immunization_fractions, infection_ratio_changes['acquaintance'], label='Acquaintance Strategy')  
    plt.xlabel('g')  
    plt.ylabel(r'$ρ{\mathrm{g}}/ρ{\mathrm{0}}$')  
    plt.legend()  
    plt.show()

def main():
    filePath = "C:\\Users\\范春\\Desktop\\week5\\twenty_years_edgelist.xlsx"
    G = network(filePath)
    print("网络生成成功！")
    '''rich_club(G)
    print("任务1完成")
    r = degree_degree(G)
    print(r)
    print("任务2完成")
    SIS_SIR(G)
    print("任务3完成")'''
    question4(G)
    
if __name__=='__main__':
    main()