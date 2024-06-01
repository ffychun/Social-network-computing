import pickle  
import matplotlib.pyplot as plt  
import numpy as np
  
# 读取pickle文件  
import numpy as np  
import matplotlib.pyplot as plt  
import pickle  
  
# 加载数据并去除NaN值  
with open('C:\\Users\\范春\\Desktop\\week5\\rich_club_coefficient.pkl', 'rb') as f:  
    data = pickle.load(f)  
  
# 提取度和对应的rich_club系数  
degrees = list(data.keys())  
#print(degrees)
coefficients = list(data.values())  
#print(coefficients)
  
plt.semilogx(degrees, coefficients)  
plt.xlabel('k')  
plt.ylabel(r'$\rho_{\mathrm{rand}}(k)$')    
plt.show()