import json
import random
from PIL import Image
import os
'''
def consistent_random_sample_json(input_file, output_file, sample_size=5000):
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 初始化抽样后的数据字典
    sampled_data = {}

    # 获取所有顶层键
    keys = list(data.keys())
    if not keys:
        return  # 如果没有键，直接返回

    # 从第一个键随机抽取数据
    first_key = keys[0]
    if isinstance(data[first_key], dict):
        sub_keys = list(data[first_key].keys())
        if len(sub_keys) >= sample_size:
            sampled_sub_keys = random.sample(sub_keys, sample_size)
        else:
            sampled_sub_keys = sub_keys  # 如果不够抽取，则全部保留
    else:
        return  # 如果第一个键的值不是字典，直接返回

    # 根据抽取的子键，从每个顶层键的字典中抽取相应的数据
    for key in keys:
        if isinstance(data[key], dict):
            sampled_data[key] = {sub_key: data[key][sub_key] for sub_key in sampled_sub_keys if sub_key in data[key]}
        else:
            sampled_data[key] = data[key]  # 非字典类型的数据直接保留

    # 将抽样后的数据保存为JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sampled_data, f, ensure_ascii=False, indent=4)

# 使用示例
input_file = "C:\\Users\\范春\\Desktop\\week12\\tabular data\\target_comment_seed2021.json"
output_file = 'output.json'
sample_size = 5000
consistent_random_sample_json(input_file, output_file, sample_size)'''

def check_image(img_path):
    try:
        with Image.open(img_path) as img:
            img.verify()  # Verify that the image is not corrupted
        return True
    except Exception:
        return False

def select_and_save(input_file, output_file, base_path):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pic_paths = data.get('pic_path',{})
    all_keys = list(pic_paths.keys())
    
    i = 0
    valid_keys = []
    for key in all_keys:
        if (i<3000):
            print(i)
            original_path = pic_paths[key]
            new_path = original_path.replace('I:', base_path, 1)
            if os.path.exists(new_path) and check_image(new_path):
                valid_keys.append(key)
                i +=1
            else:
                print(f"Invalid or non-existent image at path: {new_path}")

    selected_data = {top_key: {sub_key: value[sub_key] for sub_key in valid_keys} for top_key, value in data.items()}

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(selected_data, f, ensure_ascii=False, indent=4)

input_file = "C:\\Users\\范春\\Desktop\\week12\\tabular data\\target_comment_seed2021.json"
output_file = 'C:\\Users\\范春\\Desktop\\week12\\sample.json'
base_path = "C:\\Users\\范春\\Desktop\\20201016ImgData\\20201016ImgData"
select_and_save(input_file, output_file, base_path)
    



