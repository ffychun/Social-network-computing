import networkx as nx
import powerlaw as pl
import matplotlib.pyplot as plt
def network_calculate(N,m):
    G = nx.barabasi_albert_graph(N,m)
    print(f"顶点数:{len(G)}\n")
    print(f"边数:{G.size()}\n")
    print(f"密度:{nx.density(G)}\n")
    print(f"平均度:{2*G.size()/len(G)}\n")
    
    print(f"网络的聚集系数1:{nx.average_clustering(G)}\n")
    print(f"网络的聚集系数2:{nx.transitivity(G)}\n")
    Ds = [G.degree[n] for n in G]
    
    fg = pl.plot_pdf(Ds, color='b',marker='o')
    fit = pl.Fit(Ds)
    print(f"alpha:{fit.power_law.alpha}")
    print(f"sigma:{fit.power_law.sigma}")
    fit.power_law.plot_pdf(color='r',linestyle='--',ax=fg,label=f'$\gamma={round(fit.power_law.alpha,2)}$, $p={round(fit.power_law.sigma,2)}$')
    fg.set_title('Powerlaw distribution')
    fg.set_xlabel('k')
    fg.set_ylabel("p(k)")
    plt.legend()
    plt.savefig(f'C:\\Users\\范春\\Desktop\\{N}.png')

Ns=[1696415,54573,47538,41773]
edges=[11095298,498202,222887,125826]

#network_calculate(54573,int(498202/54573))
#network_calculate(47538,int(222887/47538))
network_calculate(41773,int(125826/41773))
