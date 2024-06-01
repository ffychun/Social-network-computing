import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
df = pd.read_excel('C:\\Users\\范春\\Desktop\\week61\\result.xlsx')

# 创建一个包含三个子图的画布
fig, axs1 = plt.subplots(1, 3, figsize=(15, 5))

# 提取mu列的数据
mu = df['mu']

# 提取modularity, coverage, performance的数据
modularity1 = df['modularity1']
modularity2 = df['modularity2']
coverage1 = df['coverage1']
coverage2 = df['coverage2']
performance1 = df['performance1']
performance2 = df['performance2']

# 绘制子图
axs1[0].plot(mu, modularity1, label='CNM')
axs1[0].plot(mu, modularity2, label='Louvain')
axs1[0].set_title('Modularity')

axs1[1].plot(mu, coverage1, label='CNM')
axs1[1].plot(mu, coverage2, label='Louvain')
axs1[1].set_title('Coverage')

axs1[2].plot(mu, performance1, label='CNM')
axs1[2].plot(mu, performance2, label='Louvain')
axs1[2].set_title('Performance')

# 添加图例
for ax in axs1.flat:
    ax.legend()

plt.tight_layout()
plt.show()

# 创建一个包含两个子图的画布
fig, axs2 = plt.subplots(1, 2, figsize=(10, 5))

# 提取rand_index, nmi的数据
rand_index1 = df['rand_index1']
rand_index2 = df['rand_index2']
nmi1 = df['nmi1']
nmi2 = df['nmi2']

# 绘制子图
axs2[0].plot(mu, rand_index1, label='CNM')
axs2[0].plot(mu, rand_index2, label='Louvain')
axs2[0].set_title('Rand Index')

axs2[1].plot(mu, nmi1, label='CNM')
axs2[1].plot(mu, nmi2, label='Louvain')
axs2[1].set_title('NMI')

# 添加图例
for ax in axs2.flat:
    ax.legend()

plt.tight_layout()
plt.show()
