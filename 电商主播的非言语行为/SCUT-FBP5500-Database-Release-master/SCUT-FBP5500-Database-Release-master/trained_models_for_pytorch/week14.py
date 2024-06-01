import os
import torch
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from torchvision import transforms
from collections import OrderedDict
from Nets import AlexNet  
import pandas as pd

# 1. 加载预训练模型
model_path = "C:\\Users\\范春\\Desktop\\week14\\pytorch-models\\alexnet.pth"  
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = AlexNet(num_classes=1)

# 从checkpoint中提取state_dict
checkpoint = torch.load(model_path, map_location=device, encoding='latin1')
state_dict = checkpoint['state_dict']

# 修改键名称以匹配模型
new_state_dict = OrderedDict()
for k, v in state_dict.items():
    name = k.replace('module.', '')  
    new_state_dict[name] = v
model.load_state_dict(new_state_dict)
model.eval()
model.to(device)

# 2. 定义图像预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 3. 计算面孔吸引力
image_dir = "C:\\Users\\范春\\Desktop\\week14\\face_seq\\face_seq"  
image_files = sorted(os.listdir(image_dir), key=lambda x: int(os.path.splitext(x)[0]))  # 按帧序号排序

scores = []
for img_file in image_files:
    img_path = os.path.join(image_dir, img_file)
    image = Image.open(img_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        score = model(image).item()
        scores.append(score)

df = pd.DataFrame({
    'Frame Number': list(range(len(scores))),
    'Attractiveness Score': scores
})

# 保存到Excel文件
output_path = "C:\\Users\\范春\\Desktop\\week14\\attractiveness_scores.xlsx"
df.to_excel(output_path, index=False)

# 4. 绘制时间序列图
plt.plot(scores)
plt.xlabel('Frame Number')
plt.ylabel('Attractiveness Score')
plt.show()
