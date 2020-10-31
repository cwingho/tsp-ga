from ga import GA
from visualizer import Visualizer

# define 10 cities
cities = [	[0.3642,0.7770],
			[0.7185,0.8312],
			[0.0986,0.5891],
			[0.2954,0.9606],
			[0.5951,0.4647],
			[0.6697,0.7657],
			[0.4353,0.1709],
			[0.2131,0.8349],
			[0.3479,0.6984],
			[0.4516,0.0488]	]

n_city = 10
n_gen = 100

visualizer = Visualizer()
visualizer.drawMap(cities)

ga = GA(cities, start_city=0, 
			population_size=20, 
			crossover_rate=0.8, 
			mutation_rate=0.1,
			elite_rate=0.1,
			seed=0)

for gen in range(n_gen):
	ga.select()
	ga.crossover()
	ga.mutation()
	ga.updateCost()
	ga.eliteSurvive()

	path, cost = ga.getBestPop()
	print('Gen:{} Best path:{} Cost:{}'.format(gen+1, path, cost))

	visualizer.append(cost)

# visualizer.draw()

visualizer.drawMap(cities)


# for i in range(n_city):
# 	ga = GA(cities, start_city=i, 
# 				population_size=20, 
# 				crossover_rate=0.8, 
# 				mutation_rate=0.1,
# 				elite_rate=0.1,
# 				seed=0)

# 	for gen in range(n_gen):
# 		ga.select()
# 		ga.crossover()
# 		ga.mutation()
# 		ga.updateCost()
# 		ga.eliteSurvive()

# 		path, cost = ga.getBestPop()
# 		print('Gen:{} Best path:{} Cost:{}'.format(gen+1, path, cost))

# 		# visualizer.append(i, cost)
# 		visualizer.multiAppend(i, cost)

# # visualizer.draw()
# visualizer.multiDraw()

