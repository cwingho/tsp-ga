import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from visualizer import Visualizer

class SPVisualizer(Visualizer):
	def __init__(self,	save_dir='./result/', 
						file_name='output',
						title='Cost',
						x_label='Generation',
						y_label='Cost/f(x)',
						n_fig=10):

		super().__init__(	save_dir=save_dir, 
							file_name=file_name,
							title=title,
							x_label=x_label,
							y_label=y_label,
							n_fig=n_fig)

	def draw(self):
		'''
		Draw a cost chart
		'''
		plt.figure(figsize=(15, 5))
		plt.plot(self.x,self.y)
		
		plt.title(self.title)
		plt.xlabel(self.x_label)
		plt.ylabel(self.y_label)

		plt.savefig(self.save_dir+'/'+self.file_name+'.png')

	def drawMap(self,cities,path_list=None,label=None,save=True,title='Map'):
		'''
		Draw a map
		'''
		padding = 0.01
		cities = np.asarray(cities)
		plt.xlim(0, 1)
		plt.ylim(0, 1)
		plt.title(title)
		plt.xlabel('x')
		plt.ylabel('y')
		plt.tight_layout()

		# draw city
		plt.scatter(cities[:,0],cities[:,1],color=self.color)

		# draw line
		if path_list:
			for i in range(len(path_list)):
				c = cities[label==i]
				path = c[path_list[i]]
				plt.plot(path[:,0],path[:,1],color=self.color_choice[i])

		for idx,c in enumerate(cities):
			plt.annotate(idx+1, (c[0]+padding,c[1]+padding))

		if save:
			plt.savefig(self.save_dir+'/map.png')

	def _drawMap(self,cities,path=None,save=True,title='Map'):
		'''
		Draw a map
		'''
		padding = 0.01
		cities = np.asarray(cities)
		plt.xlim(0, 1)
		plt.ylim(0, 1)
		plt.title(title)
		plt.xlabel('x')
		plt.ylabel('y')
		plt.tight_layout()

		_path = np.zeros(len(path)+1,dtype=np.int32)
		_path[:-1] = path
		_path[-1] = path[0]

		# draw line
		path = cities[_path]
		plt.plot(path[:,0],path[:,1],color='k')

		if save:
			plt.savefig(self.save_dir+'/map.png')

	def save(self):
		plt.savefig(self.save_dir+'/map.png')		

	def multiDrawMap(self,cities,path=None):
		'''
		Draw multiple map
		'''

		# append the starting city to the end to form a close loop
		path = np.asarray(path)
		_path = np.zeros((len(path),len(path)),dtype=np.int32)
		_path = path

		plt.figure(figsize=(15, 12))
		for i in range(self.n_fig):
			plt.subplot(4,3,i+1)
			plt.subplots_adjust(hspace = 0.25)
			self.drawMap(cities=cities,path=_path[i],save=False,title="Starting city {}".format(i+1))

		plt.savefig(self.save_dir+'/multi_route_map.png')
		




