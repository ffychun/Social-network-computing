import matplotlib.pyplot as plt

# 读取三个txt文件的数据
filePath1 = "C:\\Users\\范春\\Desktop\\kuramoto-master\\kuramoto-master\\kuramoto\\kuramoto\\result\\data\\500_100_3.txt"
filePath2 = "C:\\Users\\范春\\Desktop\\kuramoto-master\\kuramoto-master\\kuramoto\\kuramoto\\result\\data\\1000_100_3.txt"
filePath3 = "C:\\Users\\范春\\Desktop\\kuramoto-master\\kuramoto-master\\kuramoto\\kuramoto\\result\\data\\2000_100_3.txt"
filePath4 = "C:\\Users\\范春\\Desktop\\kuramoto-master\\kuramoto-master\\kuramoto\\kuramoto\\result\\data\\4000_100_3.txt"
data_files = [filePath1,filePath2,filePath3,filePath4]

colors = ['red', 'green', 'blue','purple']  # 每个文件对应的颜色
labels = ['N=500','N=1000','N=2000','N=4000']

plt.figure()

for i, file in enumerate(data_files):
    with open(file, 'r') as f:
        lines = f.readlines()[1:]  # 跳过第一行
        coupling = []
        order_parameter = []
        for line in lines:
            line = line.strip().split()
            coupling.append(float(line[0]))
            order_parameter.append(float(line[1]))
        plt.plot(coupling, order_parameter, marker='o', linestyle='-', color=colors[i], label=labels[i])

plt.xlabel('lamda')
plt.ylabel('r')
plt.legend()
plt.grid(True)
plt.show()
