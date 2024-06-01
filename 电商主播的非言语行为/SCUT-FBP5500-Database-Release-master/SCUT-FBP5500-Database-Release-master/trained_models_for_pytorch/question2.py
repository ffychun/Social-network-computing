import pandas as pd
import matplotlib.pyplot as plt

# 读取之前保存的 Excel 文件
input_path = "C:\\Users\\范春\\Desktop\\week14\\attractiveness_scores.xlsx"
df = pd.read_excel(input_path)

# 计算移动平均
window_size = 5
df['Moving Average'] = df['Attractiveness Score'].rolling(window=window_size).mean()

# 可视化吸引力得分及其移动平均
plt.figure(figsize=(10, 5))
plt.plot(df['Frame Number'], df['Attractiveness Score'], label='Attractiveness Score')
plt.plot(df['Frame Number'], df['Moving Average'], label='Moving Average', linestyle='--', color='red')

plt.xlabel('Frame Number')
plt.ylabel('Attractiveness Score')
plt.title('Attractiveness Score Over Time with Key Points')
plt.legend()
plt.show()

# 保存结果到Excel文件
output_path = "C:\\Users\\范春\\Desktop\\week14\\attractiveness_scores_with_moving_average_and_top_points.xlsx"
df.to_excel(output_path, index=False)
