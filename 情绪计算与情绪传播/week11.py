import pymongo
from pymongo import MongoClient
import networkx as nx
import scipy.stats
import random
import json
from collections import defaultdict
import matplotlib.pyplot as plt

client = MongoClient("mongodb://localhost:27017")  
db = client['week11']  
collection = db['week11'] 

def generateGraph(filePath):
    emotionsDic = {}
    G = nx.Graph()  
    with open(filePath, 'r') as file:
        for line in file:
            user1, user2, weight, emotions = line.strip().split('\t')
            G.add_edge(int(user1), int(user2)) 
            emotions = list(map(int, emotions[1:-1].split(',')))
            total_sum = sum(emotions)
            if total_sum == 0:
                emotions = [0, 0, 0, 0]
            else:
                emotions = [x / total_sum for x in emotions]
            emotionsDic[int(user1)] = emotions
    return G, emotionsDic

def shortestPathLength(G):
    for node in G.nodes:
        paths = nx.single_source_shortest_path_length(G, node)
        str_paths = {str(k): v for k, v in paths.items()} 
        collection.insert_one({'node': str(node), 'distances': dict(str_paths)})
    
    return collection

def get_random_samples(collection, distance):
    cursor = collection.find({})
    all_distances = []
    
    for doc in cursor:
        node1 = int(doc['node'])
        distances = {int(k): v for k, v in doc['distances'].items() if v == distance}
        for node2 in distances.keys():
            all_distances.append((node1, node2))

    return all_distances

def create_emotion_list():
    return ([], [])

def calculate_average_correlations(collection, emotionsDic, num_samples, num_repetitions):
    correlation_results = {emotion: {h: [] for h in range(1, 4)} for emotion in ['anger', 'disgust', 'happiness', 'sadness']}  
    for h in range(1, 4): 
        all_distances = get_random_samples(collection, h)
        for i in range(num_repetitions):  
            if len(all_distances)<num_samples:
                samples = all_distances
            else:
                samples = random.sample(all_distances, num_samples)

            emotion_data = defaultdict(create_emotion_list, {emotion: create_emotion_list() for emotion in ['anger', 'disgust', 'happiness', 'sadness']})

            for node1, node2 in samples:
                for emotion, idx in zip(['anger', 'disgust', 'happiness', 'sadness'], range(4)):
                    emotion_data[emotion][0].append(emotionsDic[node1][idx])
                    emotion_data[emotion][1].append(emotionsDic[node2][idx])
            
            for emotion in emotion_data.keys():
                pearson_corr, _ = scipy.stats.pearsonr(emotion_data[emotion][0], emotion_data[emotion][1])
                spearman_corr, _ = scipy.stats.spearmanr(emotion_data[emotion][0], emotion_data[emotion][1])
                correlation_results[emotion][h].append((pearson_corr, spearman_corr))
    
    average_correlation_results = {emotion: {h: (0, 0) for h in range(1, 4)} for emotion in ['anger', 'disgust', 'happiness', 'sadness']}  
    for emotion in correlation_results.keys():
        for h in correlation_results[emotion].keys():
            if correlation_results[emotion][h]:
                avg_pearson = sum([x[0] for x in correlation_results[emotion][h]]) / len(correlation_results[emotion][h])
                avg_spearman = sum([x[1] for x in correlation_results[emotion][h]]) / len(correlation_results[emotion][h])
                average_correlation_results[emotion][h] = (avg_pearson, avg_spearman)
    
    return average_correlation_results

def main():
    filePath = "C:\\Users\\范春\\Desktop\\week11\\weibograph.txt"  
    G, emotionsDic = generateGraph(filePath)
    collection = shortestPathLength(G)
    average_correlation_results = calculate_average_correlations(collection, emotionsDic, 1000,50)

    results_path = 'C:\\Users\\范春\\Desktop\\week11\\correlation_results.json'
    with open(results_path, 'w') as f:
        json.dump(average_correlation_results, f)

    plt.figure(figsize=(10, 6))
    for emotion in ['anger', 'disgust', 'happiness', 'sadness']:
        plt.plot(range(1, 4), [corr[0] for corr in average_correlation_results[emotion].values()], label=emotion, marker='o')
    plt.xlabel('Distance (h)')
    plt.ylabel('Pearson Correlation')
    plt.legend()
    plt.savefig('C:\\Users\\范春\\Desktop\\week11\\pearson_correlation.png')
    plt.show()

    plt.figure(figsize=(10, 6))
    for emotion in ['anger', 'disgust', 'happiness', 'sadness']:
        plt.plot(range(1, 4), [corr[1] for corr in average_correlation_results[emotion].values()], label=emotion, marker='o')
    plt.xlabel('Distance (h)')
    plt.ylabel('Spearman Correlation')
    plt.legend()
    plt.savefig('C:\\Users\\范春\\Desktop\\week11\\spearman_correlation.png')
    plt.show()

if __name__ == '__main__':
    main()