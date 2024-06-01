import networkx as nx
import matplotlib.pyplot as plt

def network(filePath):
    '''
    生成网络
    '''
    G = nx.Graph()
    with open(filePath,'r') as f:
        lines = f.readlines()
        for line in lines[4:]:
            row = line.strip().split('\t')
            G.add_edge(int(row[0]),int(row[1]))

    return G

def giant_component_ratio(G):
    '''
    计算最大连通分支和第二连通分支占网络规模的比值
    '''
    results = []
    ccs = sorted(nx.connected_components(G), key=len,reverse=True)
    largest_cc = ccs[0]
    giant_component_size = len(largest_cc)
    network_size = len(G.nodes())
    giant_component_ratio = giant_component_size / network_size
    results.append(giant_component_ratio)
    if (len(ccs)>1):
        second_cc = ccs[1]
        second_component_size = len(second_cc)/network_size
        results.append(second_component_size)
    else:
        print("该网络连通，无第二大连通分支！")

    return results

def importanceIndex(G):
    '''
    计算节点的重要性的各个指标
    '''
    degree_centrality = nx.degree_centrality(G) #度中心性
    nbc = nx.betweenness_centrality(G) #介数
    Cc = nx.closeness_centrality(G, u=None, distance=None, wf_improved=True) #接近中心性
    core = nx.core_number(G) #核数

    return [degree_centrality,nbc,Cc,core]

def attack_network(G, importance_measure,px):
    nodes_sorted = sorted(importance_measure, key=importance_measure.get, reverse=True)
    num_nodes_to_remove = int(len(nodes_sorted)*px)
    nodes_to_remove = nodes_sorted[:num_nodes_to_remove]

    G_copy = G.copy()
    G_copy.remove_nodes_from(nodes_to_remove)
    ratio = giant_component_ratio(G_copy)
    ratio1 = ratio[0]
    ratio2 = ratio[1]

    return ratio1,ratio2


def main():
    filePath = "C:\\Users\\范春\\Desktop\\week3\\p2p-Gnutella04.txt\\p2p-Gnutella04.txt"
    G = network(filePath)
    importanceindex = importanceIndex(G)
    item = ["degree_centrality","nbc","Cc","core"]
    for j in range(4):
        resultPath = f"C:\\Users\\范春\\Desktop\\{item[j]}.txt"
        with open(resultPath , 'w') as result_file:
            for i in range(1,81):
                px = i*0.01
                ratio1, ratio2 = attack_network(G,importanceindex[j],px)
                result_file.write(f"{px}\t{ratio1}\t{ratio2}\n")
            print(f"{item[j]}成功\n")
    
if __name__=="__main__":
    main()