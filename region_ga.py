import numpy as np
import math

class RGA():
	def __init__(self,	cities, 
						start_city=0, 
						population_size=10, 
						crossover_rate=0.8, 
						mutation_rate=0.1, 
						elite_rate=0.1,
						atsp=False,
						seed=0):

		# set seed for reproducing result
		np.random.seed(seed)

		self.cities = np.asarray(cities)
		self.pop_size = population_size
		self.co_rate = crossover_rate
		self.mut_rate = mutation_rate
		self.elite_rate = elite_rate
		self.start = start_city

		# no. of elite that reintroduce in next generation
		self.n_elite = math.floor(self.pop_size*self.elite_rate)

		# the size of the chromosome is the no. of cities
		self.dna_size = len(cities)

		# advanced setting
		# asymmetric traveling salesman problem
		self.atsp = atsp

		# buffer the result of distance between 2 cities
		# to save computation
		self.dist = self.computeDist(self.dna_size)

		# init populations
		self.pop = self.initPop(self.pop_size, self.dna_size, self.start)

		# compute the fitness of each individual
		self.cost = self.computeCost()

	def initPop(self, pop_size, dna_size, start_city):
		'''
		initial the individuals
		'''
		pop = np.zeros((pop_size,dna_size), dtype=int)
		for i in range(pop_size):
			pop[i] = np.arange(dna_size)
			
		return pop

	def computeCost(self):
		cost = np.zeros(self.pop_size)
		for i in range(self.pop_size):
			x = self.pop[i][1::2]
			y = np.roll(self.pop[i], -1)[1::2]
			cost[i] = np.sum(self.dist[x,y])
		return cost

	def crossover(self):
		'''
		crossover: male and female exchange the dqa
		'''
		for i in range(self.pop_size):
			male = self.pop[i]

			if np.random.rand() < self.co_rate:
				_i = np.random.randint(self.pop_size)
				female = self.pop[_i]

				pos = np.random.randint(low=2,high=self.dna_size,size=2)
				head = min(pos)
				tail = max(pos)

				if head%2 !=0:
					head -= 1

				if tail%2 !=0:
					tail -= 1

				# pattern should keep in both male and female
				keep_dna = male[head:tail]
				male_exchange_dna_mask = ~np.isin(male, keep_dna)
				# male dna for exchange
				male_exchange_dna = male[male_exchange_dna_mask]

				female_exchange_dna_mask = ~np.isin(female, keep_dna)
				# female dna for exchange
				female_exchange_dna = female[female_exchange_dna_mask]

				# exchange the dna
				male[male_exchange_dna_mask] = female_exchange_dna
				female[female_exchange_dna_mask] = male_exchange_dna

	def mutation(self):
		'''
		mutation by swap 2 city
		'''
		for i in range(self.pop_size):
			if np.random.rand() < self.mut_rate:
				pos = np.random.randint(low=2,high=self.dna_size,size=1)

				if pos%2 !=0:
					pos -= 1

				temp = self.pop[i,pos]
				self.pop[i,pos] = self.pop[i,pos+1]
				self.pop[i,pos+1] = temp

		for i in range(self.pop_size):
			if np.random.rand() < self.mut_rate:
				pos = np.random.randint(low=2,high=self.dna_size,size=2)

				if pos[0]%2 !=0:
					pos[0] -= 1

				if pos[1]%2 !=0:
					pos[1] -= 1

				temp1 = self.pop[i,pos[0]]
				temp2 = self.pop[i,pos[0]+1]

				self.pop[i,pos[0]] = self.pop[i,pos[1]]
				self.pop[i,pos[0]+1] = self.pop[i,pos[1]+1]

				self.pop[i,pos[1]] = temp1
				self.pop[i,pos[1]+1] = temp2

		
				




