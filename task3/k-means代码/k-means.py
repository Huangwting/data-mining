import random
import numpy as np
import matplotlib.pyplot as plt

#从文件读取数据
def read_data(file_path):
    melons = []
    try:
        with open(file_path, 'r') as f:
            for line in f: #将每一行拆分为值，转换为整数，并加到列表中
                melons.append(np.array(line.split(' ')).astype(np.int32))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        exit()
    return melons

#随机初始化中心点，并输出
def initialize_mean_vectors(melons, k):
    mvectors = random.sample(melons, k)
    for v in mvectors: #循环输出
        print(v)
    return mvectors

#基于当前聚类中心，将数据点分配给聚类
def assign_clusters(melons, mean_vectors):
    clusters = [[] for _ in range(len(mean_vectors))]
    for melon in melons:
        c = np.argmin([np.linalg.norm(melon - vec, ord=2) for vec in mean_vectors]) #使用Euclidean距离查找最接近的聚类中心的索引
        clusters[c].append(melon) #加到相应的聚类
    return clusters

#基于当前聚类分配，更新聚类中心
def update_mean_vectors(clusters):
    new_mean_vectors = [np.mean(cluster, axis=0) for cluster in clusters]
    return new_mean_vectors

#kmeans主函数
def k_means_clustering(melons, k, round_limit=10, threshold=1e-10):
    rnd = 0
    mean_vectors = initialize_mean_vectors(melons, k) #初始化


    while True:
        rnd += 1
        change = 0
        clusters = assign_clusters(melons, mean_vectors) #根据当前聚类中心进行分配

        new_mean_vectors = update_mean_vectors(clusters) #基于当前聚类分配更新聚类中心


        for i in range(k): #计算聚类中心的变化
            change += np.linalg.norm(mean_vectors[i] - new_mean_vectors[i], ord=2)
        
        mean_vectors = new_mean_vectors #用新值更新聚类中心

        #在第一次迭代后输出聚类中心
        if rnd == 1:
            for v in mean_vectors:
                print(v)

        if rnd > round_limit or change < threshold: #停止
            break

    print('最终迭代%d轮'%rnd)
    return clusters

#绘制聚类函数
def plot_clusters(clusters, colors):
    for i, col in enumerate(colors):
        for melon in clusters[i]:
            plt.scatter(melon[0], melon[1], color=col)

    plt.show()

#文件具体地址
file_path = 'f:/test.txt'
melons_data = read_data(file_path)

k_value = 3
final_clusters = k_means_clustering(melons_data, k_value)

colors_list = ['red', 'green', 'blue']
plot_clusters(final_clusters, colors_list)

