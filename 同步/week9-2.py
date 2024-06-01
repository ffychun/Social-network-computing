import os
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
from my_kuramoto import Kuramoto
from multiprocessing import Pool

def run_simulation(N):
    print('N: ',N)
    random.seed(3407)
    m = 8
    G = nx.barabasi_albert_graph(N, m)
    G_mat = nx.to_numpy_array(G)
    natfreqs = np.random.normal(0, 1, N)
    coupling_vals = np.linspace(0, 0.2, 10)
    angles_vec = np.random.uniform(-np.pi, np.pi, N)
    
    runs = []
    for coupling in coupling_vals:
        print('N and coupling：'+str(N)+'  '+str(coupling))
        model = Kuramoto(coupling=coupling, dt=0.01, T=100, n_nodes=N, natfreqs=natfreqs)
        act_mat = model.run(adj_mat=G_mat, angles_vec=angles_vec)
        runs.append(act_mat)
    runs_array = np.array(runs)

    # 计算并返回结果
    results = []
    for i, coupling in enumerate(coupling_vals):
        r_mean = np.mean([model.phase_coherence(vec) for vec in runs_array[i, :, -1000:].T])
        results.append((coupling, r_mean))

    # 保存数据到文件
    data_filename = f'result/data/{N}_100_3.txt'
    np.savetxt(data_filename, results, fmt='%.5f', header='Coupling, Order Parameter')
 
    return N, results

def plot_results(results):
    plt.figure()
    for result in results:
        N, data = result
        couplings, r_means = zip(*data)
        plt.scatter(couplings, r_means, s=20, alpha=0.7, label=f'N={N}')
    plt.grid(linestyle='--', alpha=0.8)
    plt.ylabel('Order parameter (R)')
    plt.xlabel(r'$\lambda$')
    plt.legend()
 
    # 确保结果文件夹存在
    if not os.path.exists('result/figure'):
        os.makedirs('result/figure')
    plt.savefig(f'result/figure/epl_results_100_3.png')
    plt.show()

if __name__ == "__main__":
    # 确保结果文件夹存在
    if not os.path.exists('result/data'):
        os.makedirs('result/data')
    
    N_values = [500, 1000, 2000, 4000]
    pool = Pool(processes=len(N_values))
    results = pool.map(run_simulation, N_values)
    pool.close()
    pool.join()
    plot_results(results)
    #run_simulation(500)
