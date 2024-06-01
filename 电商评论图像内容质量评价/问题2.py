import json
import os
from collections import defaultdict
import itertools
import networkx as nx
import matplotlib.pyplot as plt
from mmdet.evaluation import get_classes  

class ObjectCoOccurrenceNetwork:
    def __init__(self, inference_output_dir, output_file, score_threshold):
        self.inference_output_dir = inference_output_dir
        self.co_occurrence_matrix = defaultdict(lambda: defaultdict(int))
        self.classes = get_classes('coco')  
        self.output_file = output_file
        self.score_threshold = score_threshold

    def parse_inference_results(self):
        for root, _, files in os.walk(self.inference_output_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        result = json.load(f)
                        labels = result.get("labels", [])
                        scores = result.get("scores", [])
                        filtered_labels = [label for label, score in zip(labels, scores) if score > self.score_threshold]
                        self.update_co_occurrence(filtered_labels)

    def update_co_occurrence(self, labels):
        unique_labels = set(labels)
        for label1, label2 in itertools.combinations(unique_labels, 2):
            self.co_occurrence_matrix[label1][label2] += 1
            self.co_occurrence_matrix[label2][label1] += 1

    def save_co_occurrence_matrix(self):
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.co_occurrence_matrix, f, ensure_ascii=False, indent=4)

    def display_network(self):
        G = nx.Graph()
        for label1, related_labels in self.co_occurrence_matrix.items():
            for label2, count in related_labels.items():
                if count > 0:
                    G.add_edge(self.classes[label1], self.classes[label2], weight=count)

        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=7000, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()

    def save_network_gexf(self, gexf_path):
        G = nx.Graph()
        for label1, related_labels in self.co_occurrence_matrix.items():
            for label2, count in related_labels.items():
                if count > 0:
                    G.add_edge(self.classes[label1], self.classes[label2], weight=count)

        largest_cc = max(nx.connected_components(G), key=len)
        H = G.subgraph(largest_cc).copy()
        nx.write_gexf(H, gexf_path)

if __name__ == '__main__':
    inference_output_dir = 'C:\\Users\\范春\\Desktop\\week12\\output' 
    output_file = 'C:\\Users\\范春\\Desktop\\week12\\output\\co_occurrence_matrix.json'
    gexf_path = 'C:\\Users\\范春\\Desktop\\week12\\output\\network0_8.gexf'
    score_threshold = 0.8

    co_occur_network = ObjectCoOccurrenceNetwork(inference_output_dir, output_file, score_threshold)
    co_occur_network.parse_inference_results()
    co_occur_network.save_co_occurrence_matrix()
    co_occur_network.display_network()
    co_occur_network.save_network_gexf(gexf_path)
