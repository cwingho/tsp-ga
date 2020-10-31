import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Visualizer():
	def __init__(self,	save_dir='./result/', 
						file_name='output',
						title='Cost',
						x_label='Generation',
						y_label='f(x)'):
		self.x = list()
		self.y = list()
		self.cnt = 1

		self.save_dir = save_dir
		self.file_name = file_name
		self.title = title
		self.x_label = x_label
		self.y_label = y_label

	def append(self,y):
		self.x.append(self.cnt)
		self.y.append(y)
		self.cnt += 1

	def draw(self):
		plt.figure(figsize=(15, 5))
		plt.plot(self.x,self.y)
		
		plt.title(self.title)
		plt.xlabel(self.x_label)
		plt.ylabel(self.y_label)

		plt.savefig(self.save_dir+'/'+self.file_name+'.png')




