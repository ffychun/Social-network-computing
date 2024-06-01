import numpy as np  
import matplotlib.pyplot as plt  
import os  
  
# 设置数据文件夹路径  
data_folder = 'C:\\Users\\范春\\Desktop\\week5\\'  
  
# 定义tau和gamma值，它们是一一对应的  
tau_values = [0.2,0.25,0.3,0.35]
gamma_values = [0.15,0.2,0.25,0.3] 
  
# 绘制SIS模型结果的大图  
def plot_SIS_results(tau_values, gamma_values):  
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))  # 创建一个2x2的子图网格  
    fig.suptitle('SIS Model Simulation Results')  # 设置大图的标题  
    for i, (tau, gamma) in enumerate(zip(tau_values, gamma_values)):  
        # 计算子图的索引  
        ax_index = i  
        ax = axs.flat[ax_index]  # 使用flat属性获取子图对象  
          
        # 构造文件名  
        filename = os.path.join(data_folder, f'SIS_tau_{tau}_gamma_{gamma}.csv')  
          
        # 读取数据  
        data = np.loadtxt(filename, delimiter=',', skiprows=1)  # skiprows=1 跳过标题行  
        t, S, I = data[:, 0], data[:, 1], data[:, 2]  
          
        # 绘制曲线  
        ax.plot(t, S, label='S')  
        ax.plot(t, I, label='I')  
          
        # 设置子图标题  
        ax.set_title(f'tau={tau}, gamma={gamma}')  
          
        # 显示图例  
        ax.legend()  
      
    # 调整子图间距  
    plt.tight_layout()  
      
    # 显示大图  
    plt.show()  
  
# 绘制SIR模型结果的大图  
def plot_SIR_results(tau_values, gamma_values):  
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))  # 创建一个2x2的子图网格  
    fig.suptitle('SIR Model Simulation Results')  # 设置大图的标题  
    for i, (tau, gamma) in enumerate(zip(tau_values, gamma_values)):  
        # 计算子图的索引  
        ax_index = i  
        ax = axs.flat[ax_index]  # 使用flat属性获取子图对象  
          
        # 构造文件名  
        filename = os.path.join(data_folder, f'SIR_tau{tau}_gamma_{gamma}.csv')  
          
        # 读取数据  
        data = np.loadtxt(filename, delimiter=',', skiprows=1)  # skiprows=1 跳过标题行  
        t, S, I, R = data[:, 0], data[:, 1], data[:, 2], data[:, 3]  
          
        # 绘制曲线  
        ax.plot(t, S, label='S')  
        ax.plot(t, I, label='I')  
        ax.plot(t, R, label='R')  
          
        # 设置子图标题  
        ax.set_title(f'tau={tau}, gamma={gamma}')  
          
        # 显示图例  
        ax.legend()  
      
    # 调整子图间距  
    plt.tight_layout()  
      
    # 显示大图  
    plt.show()

plot_SIS_results(tau_values,gamma_values)
plot_SIR_results(tau_values,gamma_values)