import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt 

# 读取Excel文件  
df = pd.read_excel("C:\\Users\\范春\\Desktop\\week7\\results2.xlsx", engine='openpyxl')  

x = df['item']
y = df['average_path_length']
y = np.log10(y)

plt.plot(x,y)

plt.xlabel('alpha')
plt.ylabel('Log10(D)')

plt.legend()
plt.show()