import networkx as nx
import math

#返回网络节点的位置信息
def read_node_coordinates():
    nodes = []
    with open("C:\\Users\\范春\\Desktop\\week4\\Nodes.txt",'r') as file:
        for line in file:
            data = line.strip().split()
            node = data[0]
            x = float(data[1])
            y = float(data[2])
            nodes.append((node,x,y))
    return nodes 

# 计算节点之间的欧氏距离
def euclidean_distance(node1, node2):
    return math.sqrt((node1[1] - node2[1])**2 + (node1[2] - node2[2])**2)

# 计算网络空间的中心位置
def calculate_center_position(nodes):
    total_x = sum(node[1] for node in nodes)
    total_y = sum(node[2] for node in nodes)
    center_x = total_x / len(nodes)
    center_y = total_y / len(nodes)
    return center_x, center_y

# 计算网络空间中心区域的少量节点
def calculate_center_nodes(num_center_nodes):
    nodes = read_node_coordinates()
    center_x, center_y = calculate_center_position(nodes)
    
    center_nodes = []
    for node in nodes:
        distance = euclidean_distance((node[0], node[1], node[2]), ('center', center_x, center_y))
        center_nodes.append((node[0], distance))
    
    center_nodes.sort(key=lambda x: x[1])  # 按距离排序
    center_nodes = center_nodes[:num_center_nodes]  # 选择距离最近的少量节点
    
    return center_nodes
    
#生成加权网络
def network(filePath):
    G = nx.Graph()
    with open(filePath,'r') as f:
        lines = f.readlines()
        for line in lines:
            row = line.strip().split()
            G.add_edge(int(row[1]),int(row[2]),weight=float(row[3]))
    return G


#移除网络空间中心区域的3个节点
def remove_center_node(G):
    center_nodes = calculate_center_nodes(3)
    remove_nodes = [int(node[0]) for node in center_nodes]
    G.remove_nodes_from(remove_nodes)
    return remove_nodes

#计算最大连通分支和第二连通分支占网络规模的比值
def component_ratio(G):
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

def Motter(G):
    print("开始")
    L0 = nx.betweenness_centrality(G) #介数
    print("初始介数计算成功")
    initial_removed_nodes = remove_center_node(G)
    results = [] #存储最大连通分量随着alpha变化而变化的情况
    
    for i in range(0,11):
        print(i)
        G_copy = G.copy()
        alpha = 0.1*i
        load_capacity = {node:(1+alpha)*load for node,load in L0.items()}
        
        t = 0
        removed_nodes = [initial_removed_nodes] #存储特定alpha下每一轮次删除的节点情况

        ratios_t =[]
        ratios = component_ratio(G_copy)
        ratios.append(t)
        ratios_t.append(ratios)
        while len(G_copy.nodes())>0:
            t +=1
            Li = nx.betweenness_centrality(G_copy)
            overloaded_nodes = [node for node in G_copy.nodes() if Li[node] > load_capacity[node]]
            if len(overloaded_nodes)==0:
                break
            else:
                G_copy.remove_nodes_from(overloaded_nodes)
                removed_nodes.append(overloaded_nodes)
            ratios = component_ratio(G_copy)
            ratios.append(t)
            ratios_t.append(ratios)
        
        result = component_ratio(G_copy)
        result.append(alpha)
        results.append(result)

        with open(f"C:\\Users\\范春\\Desktop\\week4\\{alpha:.1f}_remove_nodes.txt","w") as f:
            for node in removed_nodes:
                f.write(f"{node}\n")

        with open(f"C:\\Users\\范春\\Desktop\\week4\\{alpha:.1f}_ratio.txt","w") as f:
            for item in ratios_t:
                if (len(item)==2):
                    f.write(f"{item[1]}\t{item[0]}\n")
                else:
                    f.write(f"{item[2]}\t{item[0]}\t{item[1]}\n")
    
    with open (f"C:\\Users\\范春\\Desktop\\week4\\result.txt","w") as f:
        for result in results:
            if (len(result)==2):
                f.write(f"{result[1]:.1f}\t{result[0]}\n")
            else:
                f.write(f"{result[2]:.1f}\t{result[0]}\t{result[1]}\n")

def main():
    filePath = "C:\\Users\\范春\\Desktop\\week4\\Edges.txt"
    G = network(filePath)
    Motter(G)

if __name__=="__main__":
    main()