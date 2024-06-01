import matplotlib.pyplot as plt
import networkx as nx

def read_removed_nodes(filePath):
    datas = []
    with open(filePath,'r') as file:
        for line in file:
            f = []
            data = line.strip()[1:-1].split('\t')
            data = data[0].split(',')
            for i in data:
                f.append(int(i))
            datas.append(f)
    return datas

#生成加权网络
def network(filePath):
    G = nx.Graph()
    with open(filePath,'r') as f:
        lines = f.readlines()
        for line in lines:
            row = line.strip().split()
            G.add_edge(int(row[1]),int(row[2]),weight=float(row[3]))
    return G

#返回网络节点的位置信息
def read_node_coordinates():
    pos = {}
    with open("C:\\Users\\范春\\Desktop\\week4\\Nodes.txt",'r',encoding='utf-8') as file:
        for line in file:
            data = line.strip().split()
            node = int(data[0])
            x = float(data[1])
            y = float(data[2])
            pos[node]=(x,y)
    return pos

def main():
    G = network("C:\\Users\\范春\\Desktop\\week4\\Edges.txt")
    pos = read_node_coordinates()
    removed_nodes = read_removed_nodes("C:\\Users\\范春\\Desktop\\week4\\0.4_remove_nodes.txt")

    options = {"node_size": 5, "alpha": 0.8}

    fig, axs = plt.subplots(4, 4, figsize=(25, 25))
    
    for i in range(4):
        for j in range(4):
            ax = axs[i, j]
            
            combined_nodes = []
            for k in range(i*4 + j + 1):
                combined_nodes += removed_nodes[k]
            
            for k in range(i*4 + j + 1):
                nx.draw_networkx_nodes(G, pos, nodelist=combined_nodes, node_color='red', ax=ax,**options)
                nx.draw_networkx_edges(G, pos, ax=ax)
            
            ax.text(0.95, 0.95, f't = {i*4 + j + 1}', horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=12, color='black')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()