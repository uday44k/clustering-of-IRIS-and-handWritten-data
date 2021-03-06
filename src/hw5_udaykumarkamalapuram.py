# -*- coding: utf-8 -*-
"""HW5_UdayKumarKamalapuram.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pbTATqpSHV429LJcOineZkSpL6HqTfQI
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()

iris_data = pd.read_table("./1649181792_01407_1604554690_4994035_1601384279_9602122_iris_new_data.txt", header=None, skip_blank_lines=False, delim_whitespace=True)

#k-mean implementation
from scipy.spatial.distance import cdist 
def kmeans_func(x, k, iter):
    idx = np.random.choice(len(x), k, replace=False)
    cent = x[idx, :] 
    dist = cdist(x, cent ,'cosine')
    pnts = np.array([np.argmin(i) for i in dist]) 
    for _ in range(iter): 
        cent = []
        for idx in range(k):
            temp_cent = x[pnts==idx].mean(axis=0) 
            cent.append(temp_cent)
 
        cent = np.vstack(cent)
        dist = cdist(x, cent ,'cosine')
        pnts = np.array([np.argmin(i) for i in dist])
    return pnts, cent

iris_cluster_labels = kmeans_func(iris_data.values,3,75)
print(iris_cluster_labels[0])
np.savetxt("irisOutData.txt",iris_cluster_labels[0],fmt="%s")

from sklearn.decomposition import PCA
pca = PCA(2)
df = pca.fit_transform(iris_data)
unique_points = np.unique(iris_cluster_labels[0])
for i in unique_points:
    plt.scatter(df[iris_cluster_labels[0] == i , 0] , df[iris_cluster_labels[0] == i , 1] , label = i)
plt.legend()
plt.show()

digit_image_data = pd.read_csv("./1649182019_5350096_1604556007_243332_1601384482_8387134_image_new_test.txt",header=None, delimiter=",")

digit_img_cluster_labels = kmeans_func(digit_image_data.values,10,75)

figure, ax = plt.subplots(2, 5, figsize=(8, 3))
centers =digit_img_cluster_labels[1].reshape(10,28,28)
for axi, center in zip(ax.flat, centers):
    axi.set(xticks=[], yticks=[])
    axi.imshow(center, interpolation='nearest', cmap=plt.cm.binary)

#Elbow graph implementation to find out optimal k

def sum_sqrd_erros(y , z):
  sum = 0 
  n = len(y)
  for i in range (1,n):
    diff = y[i] - z[i] 
    sqrd_diff = diff**2  
    sum = sum + sqrd_diff  
  return sum/n  

distrtn = []

K = [2,4,6,8,10,12,14,16,18,20]
y = kmeans_func(digit_image_data.values,10,50)    
for k in K:
    kmeanModelObserved = kmeans_func(digit_image_data.values,k,50)    
    model=kmeanModelObserved[0]
    distrtn.append(sum_sqrd_erros(y[0],model))


plt.figure()
plt.plot(K, distrtn, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Optimal K with Elbow Graph method')
plt.show()

#PCA AND t-SNE dimentionality reduction

pca = PCA(n_components=75)
pca_data = pca.fit_transform(digit_image_data)
print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2,perplexity=8,verbose=1,n_iter=250)
tsne_pca_data = tsne.fit_transform(pca_data)

digit_clster_labels = kmeans_func(tsne_pca_data,10,150)
print((digit_clster_labels[0]))

unique_labels = np.unique(digit_clster_labels[0])
for i in unique_labels:
    plt.scatter(tsne_pca_data[digit_clster_labels[0] == i , 0] , tsne_pca_data[digit_clster_labels[0] == i , 1] , label = i)

plt.legend(loc='center right')
plt.figure(figsize=(20,20))
plt.show()

np.savetxt("digitoutputfile.txt",digit_clster_labels[0],fmt="%s")