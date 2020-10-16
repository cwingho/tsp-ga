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
		self.dist = self.computeDist(self.dna_size)

		# init populations
		self.pop = self.initPop(self.pop_size, self.dna_size, self.start)

		# compute the fitness of each individual
		self.fitness = self.computeFit()

	def initPop(self, pop_size, dna_size, start_city):
		'''
		initial the individuals
		'''
		pop = np.zeros((pop_size,dna_size), dtype=int)
		for i in range(pop_size):
			pop[i] = np.arange(dna_size)
			np.random.shuffle(pop[i])

			# put the start node at the begining
			if pop[i][0] != start_city:
				pop[i][pop[i] == start_city] = pop[i][0]
				pop[i][0] = start_city
		return pop

	def computeDist(self, dna_size):
		'''
		compute the distance between each city and save in buffer
		'''
		dist = np.zeros((dna_size, dna_size))
		for i in range(dna_size):
			for j in range(i+1, dna_size):
				d = np.sqrt(np.square(self.cities[i][0]-self.cities[j][0])+
						np.square(self.cities[i][1]-self.cities[j][1]))
				dist[i][j] = d
				dist[j][i] = d
		return dist

	def computeFit(self):
		fitness = np.zeros(self.pop_size)
		for i in range(self.pop_size):
			x = self.pop[i]
			y = np.roll(self.pop[i], -1)
			fitness[i] = np.sum(self.dist[x,y])
		return fitness




