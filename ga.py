import numpy as np
import math
class GA():
	def __init__(self, cities, start_city=0, population_size=10, crossover_rate=0.8, mutation_rate=0.1, seed=0):
		np.random.seed(seed)

		self.cities = np.asarray(cities)
		self.pop_size = population_size
		self.co_rate = crossover_rate
		self.mut_rate = mutation_rate
		self.start = start_city

		# the size of the chromosome is the no. of cities
		self.dna_size = len(cities)

		# buffer the result of distance between 2 cities
		# to save computation
		self.distance = dict()

		# init populations
		self.pop = self.initPop(self.pop_size, self.dna_size, self.start)

	def initPop(self, pop_size, dna_size, start_city):
		'''
		initial the individuals
		'''
		pop = np.zeros((pop_size,dna_size))
		for i in range(pop_size):
			pop[i] = np.arange(dna_size)
			np.random.shuffle(pop[i])
		return pop

	def computeDist(self):
		'''
		compute the distance between each city and save in buffer
		'''
		self.dist = np.zeros((self.dna_size, self.dna_size))
		for i in range(self.dna_size):
			for j in range(i+1, self.dna_size):
				dist = np.sqrt(np.square(self.cities[i][0]-self.cities[j][0])+
						np.square(self.cities[i][1]-self.cities[j][1]))

				self.dist[i][j] = dist
				self.dist[j][i] = dist

