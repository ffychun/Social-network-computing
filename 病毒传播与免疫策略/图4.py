import pandas as pd
import matplotlib.pyplot as plt

# 读取Excel文件
df = pd.read_excel('C:\\Users\\范春\\Desktop\\week5\\simulation_results.xlsx')

# 提取数据
g = df['g']
random_data = df['random']
target_data = df['target']
acquaintance_data = df['acquaintance']

# 绘制图形
plt.figure(figsize=(10, 6))
plt.plot(g, random_data, label='random', marker='o')
plt.plot(g, target_data, label='target', marker='s')
plt.plot(g, acquaintance_data, label='acquaintance', marker='^')

# 添加标题和标签
plt.title('Infection Ratio Changes')
plt.xlabel('g')
plt.ylabel('Infection Ratio')
plt.legend()

# 显示网格
plt.grid(True)

# 显示图形
plt.show()
