import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
  
# 读取Excel文件  
df = pd.read_excel("C:\\Users\\范春\\Desktop\\week7\\results1.xlsx", engine='openpyxl')  
  
# 提取x轴和y轴的数据  
x = df['N']  
y_rw = df['RW']  
y_max_degree = df['max_degree']  
y_min_degree = df['min_degree']  
y_preferential_attachment = df['preferential_attachment']  
  
# 对x和y取对数  
x_log = np.log10(x)  
y_rw_log = np.log10(y_rw)  
y_max_degree_log = np.log10(y_max_degree)  
y_min_degree_log = np.log10(y_min_degree)  
y_preferential_attachment_log = np.log10(y_preferential_attachment)  
  
# 创建一个新的图形窗口  
plt.figure(figsize=(10, 8))  
  
# 绘制RW与N的关系（取对数后）  
plt.plot(x_log, y_rw_log, label='RW')  
  
# 绘制max_degree与N的关系（取对数后）  
plt.plot(x_log, y_max_degree_log, label='Max Degree')  
  
# 绘制min_degree与N的关系（取对数后）  
plt.plot(x_log, y_min_degree_log, label='Min Degree')  
  
# 绘制preferential_attachment与N的关系（取对数后）  
plt.plot(x_log, y_preferential_attachment_log, label='Preferential Attachment')  
  
# 设置图形标题和轴标签（使用对数后的标签）  
plt.xlabel('Log10(N)')  
plt.ylabel('Log10(D)')  
  
# 显示图例  
plt.legend()  
  
# 显示图形  
plt.show()