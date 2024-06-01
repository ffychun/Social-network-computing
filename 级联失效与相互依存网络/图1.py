import matplotlib.pyplot as plt

x_values = []
y_values = []
with open("C:\\Users\\范春\\Desktop\\week4\\result.txt", 'r') as file:
    for line in file:
        data = line.strip().split()
        alpha = float(data[0])
        p = float(data[1])
        x_values.append(alpha)
        y_values.append(p)

plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, marker='^', markersize=8, linestyle='-', label='Data Points')
plt.xlabel('Alpha')
plt.ylabel('P')
plt.legend()
plt.grid(True)
plt.show()
