import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

class Kmean():
	def __init__(self, cities, n_cluster=3, seed=0, save_dir='./result/',):
		self.cities = np.asarray(cities)
		self.n_cluster = n_cluster
		self.seed = seed

		self.save_dir = save_dir
	
	def clustering(self):
		self.kmeans = KMeans(n_clusters=self.n_cluster, 
						random_state=self.seed).fit(self.cities)

	def getLabel(self):
		return self.kmeans.labels_
	