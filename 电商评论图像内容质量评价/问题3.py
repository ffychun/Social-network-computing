import json
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mmdet.evaluation import get_classes  

class ImageTextConsistency:
    def __init__(self, inference_output_dir, sample_json_path, score_threshold):
        self.inference_output_dir = inference_output_dir
        self.sample_json_path = sample_json_path
        self.score_threshold = score_threshold
        self.classes = get_classes('coco')  
        self.image_results = {}
        self.comments = {}

    def load_sample_json(self):
        with open(self.sample_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.comments = data['content']
            self.image_paths = data['pic_path']

    def load_inference_results(self):
        for root, _, files in os.walk(self.inference_output_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        result = json.load(f)
                        labels = result.get("labels", [])
                        scores = result.get("scores", [])
                        filtered_labels = [label for label, score in zip(labels, scores) if score > self.score_threshold]
                        pic_id = os.path.basename(file_path).split('.')[0]
                        self.image_results[pic_id] = filtered_labels

    def calculate_consistency(self, comment, detected_labels):
        detected_objects = set([self.classes[label] for label in detected_labels])
        words = set(re.findall(r'\b\w+\b', comment.lower()))
        common_objects = detected_objects & words
        return len(common_objects) / len(detected_objects) if detected_objects else 0

    def analyze_consistency(self):
        consistencies = []
        for pic_id, comment in self.comments.items():
            detected_labels = self.image_results.get(pic_id, [])
            consistency = self.calculate_consistency(comment, detected_labels)
            consistencies.append((pic_id, consistency))
        return consistencies

    def save_consistency_results(self, output_file, consistencies):
        df = pd.DataFrame(consistencies, columns=['pic_id', 'consistency'])
        df.to_csv(output_file, index=False)

if __name__ == '__main__':
    inference_output_dir = 'C:\\Users\\范春\\Desktop\\week12\\output'  
    sample_json_path = 'C:\\Users\\范春\\Desktop\\week12\\sample.json' 
    output_consistency_file = 'C:\\Users\\范春\\Desktop\\week12\\output\\consistency_results.csv'
    score_threshold = 0.6

    consistency_analyzer = ImageTextConsistency(inference_output_dir, sample_json_path, score_threshold)
    consistency_analyzer.load_sample_json()
    consistency_analyzer.load_inference_results()
    consistencies = consistency_analyzer.analyze_consistency()
    consistency_analyzer.save_consistency_results(output_consistency_file, consistencies)
   
