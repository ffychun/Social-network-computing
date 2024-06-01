import matplotlib.pyplot as plt

# 读取txt文件并提取数据
def read_txt(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        data = [[float(x) for x in line.strip().split()] for line in lines]
    return data

# 绘制图形
def plot_graph(file_names,names):
    fig, axs = plt.subplots(2, figsize=(10, 8))

    for i, file_name in enumerate(file_names):
        data = read_txt(file_name)
        f = [row[0] for row in data]
        P1 = [row[1] for row in data]
        P2 = [row[2] for row in data]
        axs[0].scatter(f, P1, label=names[i])
        axs[1].scatter(f, P2, label=names[i])

    axs[0].set_title('giant_component_size')
    axs[0].set_xlabel('f')
    axs[0].set_ylabel('P1')
    axs[0].legend()

    axs[1].set_title('second_component_size')
    axs[1].set_xlabel('f')
    axs[1].set_ylabel('P2')
    axs[1].legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    file_names = ["C:\\Users\\范春\\Desktop\\degree_centrality.txt", "C:\\Users\\范春\\Desktop\\nbc.txt", "C:\\Users\\范春\\Desktop\\Cc.txt", "C:\\Users\\范春\\Desktop\\core.txt"]
    names = ["degree_centrality","nbc","Cc","core"]
    plot_graph(file_names,names)
