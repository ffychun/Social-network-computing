import json
import os
from mmengine.logging import print_log
from mmdet.apis import DetInferencer
from mmdet.evaluation import get_classes
class SimpleImageInference:
    def __init__(self, input_json, output_dir, output_json,alpha):
        self.input_json = input_json
        self.output_dir = output_dir
        self.output_json = output_json
        self.model_config = "C:\\MMDetection_GPU\\mmdetection-main\\mmdetection-main\\rtmdet_tiny_8xb32-300e_coco.py"
        self.weights = "C:\\MMDetection_GPU\\mmdetection-main\\mmdetection-main\\rtmdet_tiny_8xb32-300e_coco_20220902_112414-78e30dcc.pth"
        self.device = 'cpu'
        self.palette = None
        self.classes = get_classes('coco') # 使用的是COCO数据集的类别
        self.alpha = alpha
        self.base_path = "C:\\Users\\范春\\Desktop\\20201016ImgData\\20201016ImgData"  

    def run_inference(self):
        with open(self.input_json, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        image_counts = input_data.get('imageCount', {})
        
        with open(self.output_json, 'w', encoding='utf-8') as f_out:
            i = 0
            for pic_id, pic_path in input_data['pic_path'].items():
                pic_path = pic_path.replace('I:', self.base_path,1)
                i += 1
                inferencer = DetInferencer(
                    model=self.model_config,
                    weights=self.weights,
                    device=self.device,
                    palette=self.palette
                )
                labels_count = [0] * len(self.classes)
                num_images = image_counts.get(pic_id, 1)
                for img_index in range(num_images):
                    img_path = pic_path.replace('\\0.jpg', f'\\{img_index}.jpg')
                    if not os.path.exists(img_path):
                        print(f"Image file {img_path} does not exist. Skipping...")
                        continue
                    try:
                        result = inferencer(
                        inputs=img_path,
                        out_dir=self.output_dir + '\\' + pic_id,
                        show=False,
                        no_save_vis=False,
                        no_save_pred=False,
                        print_result=True,
                        batch_size=1,
                        pred_score_thr=0.3
                        )
                    except Exception as e:
                        print(f"Error processing image {img_path}: {str(e)}")
                        continue
                    for item in result['predictions']:
                        for label, score in zip(item['labels'],item['scores']):
                            if score > self.alpha: # 根据阈值判断
                                labels_count[label] += 1
                labels_binary = [1 if count > 0 else 0 for count in labels_count]
                results_dict = dict(zip(self.classes, labels_binary))
                f_out.write(f'{pic_id}: {json.dumps(results_dict)}\n')
                print(f'{i} is ok')

if __name__ == '__main__':
    input_json_path = "C:\\Users\\范春\\Desktop\\week12\\sample.json"
    output_directory = 'C:\\Users\\范春\\Desktop\\week12\\output'
    output_json_path = 'C:\\Users\\范春\\Desktop\\week12\\output\\data\\output0.txt'
    alpha = 0 # 这里不筛选，建立共现网络时再筛选
    inference = SimpleImageInference(input_json_path, output_directory, output_json_path,alpha)
    inference.run_inference()





