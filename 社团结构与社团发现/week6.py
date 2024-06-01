import networkx as nx
import community as community_louvain
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score
import pandas as pd
from networkx.readwrite import gexf  

#生成一定规模的网络
def generateG(n, tau1, tau2, mu):
    return nx.LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=5,min_community=10,max_community=50)
    
 

def CNM(G):
    partition = nx.community.greedy_modularity_communities(G)
    communities_list = [set(comm) for comm in partition]
    print("CNM Successfully!")
    return communities_list

def Louvain(G):
    partition = nx.community.louvain_communities(G)
    print("Louvain Successfully!")
    return partition


def evaluationIndicators(G, communities):
    # 计算模块度和其他社区质量指标  
    modularity = nx.community.modularity(G, communities)  
    print(modularity)
    print("模块度计算成功")  
      
    coverage, performance = nx.community.partition_quality(G, communities)
    print(coverage,performance)
    print("coverage, performance计算成功")

    labels_true = [None]*len(G)
    i=0
    for node, data in G.nodes(data=True):
        node_communities = data['community']
        for item in node_communities:
            labels_true[item] = i
        i+=1
    
    labels_pred = [None] * len(G)
    for idx, community in enumerate(communities):
        for node in community:
            labels_pred[node] = idx
    
    rand_index = adjusted_rand_score(labels_true,labels_pred)  
    print(rand_index)
    print("rand_index计算成功")

    nmi = normalized_mutual_info_score(labels_true,labels_pred)  
    print(nmi)
    print("nmi计算成功")
    return modularity, coverage, performance, rand_index, nmi,labels_pred

def add_communities_to_graph(G, communities):
    for community_id, community in enumerate(communities):
        for node in community:
            G.nodes[node]['community'] = community_id

def main():
    n = 1000
    tau1 = 3
    tau2 = 1.5
    # 初始化列表来保存结果  
    results = []  
    
    for i in range(1,10):  
        mu = 0.1*i
        print(mu)
        G = generateG(n, tau1, tau2, mu)  
        print("网络生成成功！")
        communitiesCNM = CNM(G)  
        communitiesLouvain = Louvain(G)  

        # 计算评价指标  
        modularity1, coverage1, performance1, rand_index1, nmi1, label_pre1 = evaluationIndicators(G, communitiesCNM)  
        modularity2, coverage2, performance2, rand_index2, nmi2, label_pre2 = evaluationIndicators(G, communitiesLouvain)  

        for node, data in G.nodes(data=True):
            if 'community' in data:
            # 将集合转换为以逗号分隔的字符串
                data['community'] = ','.join(str(community) for community in data['community'])
        gexf_path = f'C:\\Users\\范春\\Desktop\\week61\\{mu:.2f}.gexf'
        nx.write_gexf(G,gexf_path)

        G1 = G.copy()
        add_communities_to_graph(G1, communitiesCNM)
        gexf_path = f'C:\\Users\\范春\\Desktop\\week61\\CNM_{mu:.2f}.gexf'
        nx.write_gexf(G1, gexf_path)

        G2 = G.copy()
        add_communities_to_graph(G2, communitiesLouvain)
        gexf_path = f'C:\\Users\\范春\\Desktop\\week61\\Louvain_{mu:.2f}.gexf'
        nx.write_gexf(G2, gexf_path)


        df1 = pd.DataFrame(list(zip(G.nodes(), label_pre1)), columns=['Node', 'Community'])
        df2 = pd.DataFrame(list(zip(G.nodes(), label_pre2)), columns=['Node', 'Community'])

        df1.to_csv(f'C:\\Users\\范春\\Desktop\\week61\\CNM{mu:.2f}.csv', index=False)
        df2.to_csv(f'C:\\Users\\范春\\Desktop\\week61\\Louvain{mu:.2f}.csv', index=False)
        # 将结果添加到列表中  
        result_row = {  
            'modularity1': modularity1,  
            'coverage1': coverage1,  
            'performance1': performance1,  
            'rand_index1': rand_index1,  
            'nmi1': nmi1,  
            'modularity2': modularity2,  
            'coverage2': coverage2,  
            'performance2': performance2,  
            'rand_index2': rand_index2,  
            'nmi2': nmi2,  
            'mu': mu  
        }  
        results.append(result_row)  
      
    # 创建DataFrame  
    df = pd.DataFrame(results)  
      
    # 设置列的顺序  
    column_order = ['mu'] + ['modularity1', 'coverage1', 'performance1', 'rand_index1', 'nmi1'] + ['modularity2', 'coverage2', 'performance2', 'rand_index2', 'nmi2']  
    df = df[column_order]  
      
    # 保存到Excel文件  
    excel_file_path = "C:\\Users\\范春\\Desktop\\week61\\result.xlsx" 
    df.to_excel(excel_file_path, index=False)  
    print(f"Results have been saved to {excel_file_path}.")

    
if __name__=="__main__":
    main()
