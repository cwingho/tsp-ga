from ga import GA
from visualizer import Visualizer
from kmean import Kmean
import numpy as np
import pandas as pd
from sp_ga import SPGA
from region_ga import RGA
from tw_ga import TWGA
from sp_visualizer import SPVisualizer

# define 10 cities
# cities = [	[0.3642,0.7770],
# 			[0.7185,0.8312],
# 			[0.0986,0.5891],
# 			[0.2954,0.9606],
# 			[0.5951,0.4647],
# 			[0.6697,0.7657],
# 			[0.4353,0.1709],
# 			[0.2131,0.8349],
# 			[0.3479,0.6984],
# 			[0.4516,0.0488]	]

# define more cities
# cities = [	[25,42],
# 			[23,40],
# 			[25,40],
# 			[21,39],
# 			[22,37],
# 			[18,36],
# 			[46,35],
# 			[16,34],
# 			[19,34],
# 			[43,34],
# 			[41,32],
# 			[14,31],
# 			[16,31],
# 			[38,31],
# 			[34,29],
# 			[37,29],
# 			[16,28],
# 			[36,28],
# 			[12,27],
# 			[14,27],
# 			[31,27],
# 			[11,25],
# 			[28,25],
# 			[30,24],
# 			[12,23],
# 			[9,22],
# 			[22,22],
# 			[25,22],
# 			[8,20],
# 			[19,20],
# 			[22,20],
# 			[19,18],
# 			[16,17],
# 			[14,16],
# 			[11,15],
# 			[6,13],
# 			[9,12],
# 			[12,8],
# 			[17,8],
# 			[9,7],
# 			[21,7],
# 			[25,7],
# 			[15,6],
# 			[29,6],
# 			[19,5],
# 			[24,5],
# 			[28,4],
# 			[32,4],
# 			[37,3],
# 			[41,3]]
# 			
# cities = [[i[0]/50,i[1]/50] for i in cities]
# cities = np.asarray(cities)

# define city with time window
df = pd.read_csv('./P1-data-text/TSPTW_dataset.txt', sep='\t')  
df.drop(['CUST NO.', 'DEMAND', 'SERVICE TIME'], axis=1, inplace=True)
normal = 50
df[['XCOORD.','YCOORD.']] = df[['XCOORD.','YCOORD.']]/normal
df[['READY TIME','DUE DATE']] = df[['READY TIME','DUE DATE']]/normal
cities = df[['XCOORD.','YCOORD.']].values
time_window = df[['READY TIME','DUE DATE']].values

n_city = len(cities)
n_gen = 10000

visualizer = Visualizer(n_fig=n_city,title='Fitness',
						x_label='Generation',
						y_label='Fitness/f(x)')
visualizer.drawMap(cities)

#######################################################
ga = TWGA(cities, time_window,
				start_city=0, 
				population_size=100, 
				crossover_rate=0.8, 
				mutation_rate=0.1,
				elite_rate=0.2,
				seed=0)

for gen in range(n_gen):
	ga.select()
	ga.crossover()
	ga.mutation()
	ga.updateCost()
	ga.updateFitness()
	ga.eliteSurvive()

	path, cost, fitness = ga.getBestPop()
	print('Gen:{} Best path:{} Cost:{} Fitness:{}'.format(gen+1, path, cost, fitness))

	visualizer.append(fitness)

visualizer.drawMap(cities,path=path)
visualizer.draw()

#######################################################
# k = Kmean(cities,n_cluster=6)
# k.clustering()
# visualizer = SPVisualizer(n_fig=n_city)
# visualizer.setColor(k.getLabel())
# visualizer.drawMap(cities)
# entry_cities = list()
# best_path = list()
# for i in range(6):
# 	c = cities[k.getLabel()==i]
# 	ga = SPGA(c, start_city=0, 
# 				population_size=20, 
# 				crossover_rate=0.8, 
# 				mutation_rate=0.1,
# 				elite_rate=0.1,
# 				atsp=False,
# 				seed=0)

# 	for gen in range(n_gen):
# 		ga.select()
# 		ga.crossover()
# 		ga.mutation()
# 		ga.updateCost()
# 		ga.eliteSurvive()

# 		path, cost = ga.getBestPop()

# 	print('Gen:{} Best path:{} Cost:{}'.format(gen+1, path+1, cost))
# 	best_path.append(path)
# 	entry_cities.append(c[path[0]])
# 	entry_cities.append(c[path[-1]])

# visualizer.drawMap(cities=cities,path_list=best_path,label=k.getLabel(),save=False)

# ga = RGA(entry_cities, start_city=0, 
# 				population_size=20, 
# 				crossover_rate=0.8, 
# 				mutation_rate=0.1,
# 				elite_rate=0.1,
# 				atsp=False,
# 				seed=0)

# for gen in range(100):
# 	ga.select()
# 	ga.crossover()
# 	ga.mutation()
# 	ga.updateCost()
# 	ga.eliteSurvive()
# 	path, cost = ga.getBestPop()

# 	print('Gen:{} Best path:{} Cost:{}'.format(gen+1, path+1, cost))


# # # visualizer.multiDraw()
# visualizer._drawMap(cities=entry_cities,path=path,save=False)
# visualizer.save()

#######################################################

# best_path = list()
# for i in range(n_city):
# 	ga = GA(cities, start_city=i, 
# 				population_size=20, 
# 				crossover_rate=0.8, 
# 				mutation_rate=0.1,
# 				elite_rate=0.1,
# 				atsp=True,
# 				seed=0)

# 	for gen in range(n_gen):
# 		ga.select()
# 		ga.crossover()
# 		ga.mutation()
# 		ga.updateCost()
# 		ga.eliteSurvive()

# 		path, cost = ga.getBestPop()

# 		visualizer.multiAppend(i, cost)

# 	print('Gen:{} Best path:{} Cost:{}'.format(gen+1, path+1, cost))
# 	best_path.append(path)

# visualizer.multiDraw()
# visualizer.multiDrawMap(cities=cities,path=best_path)

