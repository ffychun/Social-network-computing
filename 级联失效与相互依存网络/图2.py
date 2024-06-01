import matplotlib.pyplot as plt

file_paths = ["C:\\Users\\范春\\Desktop\\week4\\0.3_ratio.txt", "C:\\Users\\范春\\Desktop\\week4\\0.4_ratio.txt", "C:\\Users\\范春\\Desktop\\week4\\0.5_ratio.txt", "C:\\Users\\范春\\Desktop\\week4\\0.6_ratio.txt"]
fig, axs = plt.subplots(2, 4, figsize=(15, 8))

for i, file_path in enumerate(file_paths):
    t_values = []
    P1_values = []
    P2_values = []

    with open(file_path, 'r') as file:
        for line in file:
            data = line.strip().split('\t')
            if (len(data)==2):
                continue
            else:
                t = int(data[0])
                P1 = float(data[1])
                P2 = float(data[2])
                t_values.append(t)
                P1_values.append(P1)
                P2_values.append(P2)

    axs[0, i].plot(t_values, P1_values, marker='o', linestyle='-', color='grey', label='P1')
    axs[1, i].plot(t_values, P2_values, marker='s', linestyle='--', color='black', label='P2')

    axs[0, i].set_title(f'alpha={(i+3)*0.1:.1f}')
    axs[0, i].set_xlabel('t')
    axs[1, i].set_xlabel('t')
    axs[0, i].set_ylabel('P1')
    axs[1, i].set_ylabel('P2')
    axs[0, i].legend()
    axs[1, i].legend()
    #axs[row, col].grid(True)

plt.tight_layout()
plt.show()
