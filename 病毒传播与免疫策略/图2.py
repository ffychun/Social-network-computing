import pickle  
import matplotlib.pyplot as plt  
import numpy as np
  
# 读取pickle文件  
with open('C:\\Users\\范春\\Desktop\\week5\\avg_neighbor_degrees.pkl', 'rb') as f:  
    degrees_to_avg_neighbors = pickle.load(f)  

degrees = list(degrees_to_avg_neighbors.keys())
avg_neighbor = [np.mean(values) for values in degrees_to_avg_neighbors.values()]

plt.scatter(degrees, avg_neighbor)
plt.xlabel('k')
plt.ylabel(r'$k{\mathrm{nn}}(k)$')
plt.show()