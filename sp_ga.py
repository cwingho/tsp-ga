import numpy as np
import math
from ga import GA

class SPGA(GA):
	def __init__(self,	cities, 
						start_city=0, 
						population_size=10, 
						crossover_rate=0.8, 
						mutation_rate=0.1, 
						elite_rate=0.1,
						atsp=False,
						seed=0):

		super().__init__(	cities, 
							start_city=start_city, 
							population_size=population_size, 
							crossover_rate=crossover_rate, 
							mutation_rate=mutation_rate, 
							elite_rate=elite_rate,
							atsp=atsp,
							seed=seed)

	def initPop(self, pop_size, dna_size, start_city):
		'''
		initial the individuals
		'''
		pop = np.zeros((pop_size,dna_size), dtype=int)
		for i in range(pop_size):
			pop[i] = np.arange(dna_size)
			np.random.shuffle(pop[i])

		return pop

	def computeCost(self):
		cost = np.zeros(self.pop_size)
		for i in range(self.pop_size):
			x = self.pop[i]
			y = np.roll(self.pop[i], -1)
			cost[i] = np.sum(self.dist[x[:-1],y[:-1]])
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

				pos = np.random.randint(low=0,high=self.dna_size,size=2)
				head = min(pos)
				tail = max(pos)

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
				pos = np.random.randint(low=0,high=self.dna_size,size=2)
				temp = self.pop[i,pos[0]]
				self.pop[i,pos[0]] = self.pop[i,pos[1]]
				self.pop[i,pos[1]] = temp				




