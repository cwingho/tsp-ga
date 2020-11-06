import numpy as np
import math

class TWGA():
	def __init__(self,	cities,
						time_window,
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
		self.time_window = np.asarray(time_window)
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

		# compute the cost of each individual
		self.cost = self.computeCost()

		# compute the fitness of each individual for time window
		self.fitness = self.computeFitness()

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
		compute the distance between each city and save for buffering
		'''
		dist = np.zeros((dna_size, dna_size))
		for i in range(dna_size):
			for j in range(i+1, dna_size):
				d = np.sqrt(np.square(self.cities[i][0]-self.cities[j][0])+
						np.square(self.cities[i][1]-self.cities[j][1]))
				dist[i][j] = d

				if self.atsp:
					dist[j][i] = d*2
				else:
					dist[j][i] = d
		return dist

	def computeCost(self):
		cost = np.zeros(self.pop_size)
		for i in range(self.pop_size):
			x = self.pop[i]
			y = np.roll(self.pop[i], -1)
			cost[i] = np.sum(self.dist[x,y])
		return cost

	def computeFitness(self):
		cost = np.zeros(self.pop_size)
		for i in range(self.pop_size):
			fit = 0
			pop = self.pop[i]
			c = 0
			for j in range(self.dna_size):
				s = pop[j]

				if j+1 >= self.dna_size:
					e = pop[0]
				else:
					e = pop[j+1]

				_c = self.dist[s,e]
				c += _c

				ready_time = self.time_window[e][0]
				due_time = self.time_window[e][1]

				if c >= ready_time and c <= due_time:
					fit += 1

			cost[i] = fit
			
		cost = cost/self.dna_size
		return cost

	def select(self):
		'''
		select the individuals based on the their cost
		lower cost, high prob to be selected
		selected individuals (elite) will replace the whole populations
		'''
		# p = np.reciprocal(self.cost)
		p = self.fitness

		idx = np.random.choice(np.arange(self.pop_size),size=self.pop_size,
								replace=True,p=p/p.sum())

		self.saveLastGen()
		self.pop = self.pop[idx]

	def saveLastGen(self):
		'''
		save the current pop and cost fot next generation
		'''
		self.last_pop = self.pop.copy()
		self.last_cost = self.cost.copy()
		self.last_fitness = self.fitness.copy()

	def eliteSurvive(self):
		# get the elite individuals
		# elite_idx = np.argsort(self.last_cost)[:self.n_elite]
		
		elite_idx = np.argsort(self.last_fitness)[::-1][:self.n_elite]

		elite_pop = self.last_pop[elite_idx]
		elite_cost = self.last_cost[elite_idx]
		elite_fitness = self.last_fitness[elite_idx]

		# get the weak individuals
		# weak_idx = np.argsort(self.cost)[::-1][:self.n_elite]
		weak_idx = np.argsort(self.fitness)[:self.n_elite]

		# replace the weak by elite
		self.pop[weak_idx] = elite_pop
		self.cost[weak_idx] = elite_cost
		self.fitness[weak_idx] = elite_fitness

	def crossover(self):
		'''
		crossover: male and female exchange the dqa
		'''
		for i in range(self.pop_size):
			male = self.pop[i]

			if np.random.rand() < self.co_rate:
				_i = np.random.randint(self.pop_size)
				female = self.pop[_i]

				pos = np.random.randint(low=1,high=self.dna_size,size=2)
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
				pos = np.random.randint(low=1,high=self.dna_size,size=2)
				temp = self.pop[i,pos[0]]
				self.pop[i,pos[0]] = self.pop[i,pos[1]]
				self.pop[i,pos[1]] = temp

	def updateCost(self):
		self.cost = self.computeCost()

	def updateFitness(self):
		self.fitness = self.computeFitness()

	# def getBestPop(self):
	# 	idx = np.argmin(self.cost)
	# 	return self.pop[idx], self.cost[idx], self.fitness[idx]

	def getBestPop(self):
		idx = np.argmax(self.fitness)
		return self.pop[idx], self.cost[idx], self.fitness[idx]
		
				




