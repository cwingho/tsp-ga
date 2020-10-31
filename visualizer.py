import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

class Visualizer():
	def __init__(self,	save_dir='./result/', 
						file_name='output',
						title='Cost',
						x_label='Generation',
						y_label='Cost/f(x)',
						n_fig=10):
		self.x = list()
		self.y = list()
		self.cnt = 1

		self.save_dir = save_dir
		self.file_name = file_name
		self.title = title
		self.x_label = x_label
		self.y_label = y_label

		self.multi_y = [list() for i in range(n_fig)]
		self.n_fig = n_fig

	def append(self,y):
		self.x.append(self.cnt)
		self.y.append(y)
		self.cnt += 1

	def multiAppend(self,idx,y):
		self.multi_y[idx].append(y)

	def draw(self):
		plt.figure(figsize=(15, 5))
		plt.plot(self.x,self.y)
		
		plt.title(self.title)
		plt.xlabel(self.x_label)
		plt.ylabel(self.y_label)

		plt.savefig(self.save_dir+'/'+self.file_name+'.png')

	def multiDraw(self):
		plt.figure(figsize=(15, 12))
		for i in range(self.n_fig):
			plt.subplot(4,3,i+1)
			plt.subplots_adjust(hspace = 0.25)
			plt.plot([c for c in range(len(self.multi_y[i]))], self.multi_y[i])

			plt.title("Starting city {}".format(i+1))
			plt.xlabel(self.x_label)
			plt.ylabel(self.y_label)

		plt.tight_layout()
		plt.savefig(self.save_dir+'/'+self.file_name+'.png')

	def drawMap(self,cities):
		cities = np.asarray(cities)
		plt.xlim(0, 1)
		plt.ylim(0, 1)
		plt.title('Map')
		plt.xlabel('x')
		plt.ylabel('y')
		plt.tight_layout()
		plt.scatter(cities[:,0],cities[:,1],color = 'r')

		for i in cities:
			plt.annotate(i+1, (cities[i][0],cities[i][1]))

		plt.savefig(self.save_dir+'/map.png')
		pass




