import matplotlib.pyplot as plt
import numpy as np 
import os 
import argparse

''' Make directory function '''
def make_dir(data_dir):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def parse_args():
	
	""" Calling the Training Statistics Data For Visualization """

	parser = argparse.ArgumentParser('Visualize your data statistics comparing multiple configurations')
	# parser.add_argument('--stats_binder', type = str , help = 'Binder where statistics files are stored')
	parser.add_argument('--generation',type = int , help = 'Generation number for visualization')
	parser.add_argument('--number_files',type = str, help = 'List of indices of configuration files you want to compare')
	# parser.add_argument('--plot_title',type=str,help = 'Title for plots')

	return parser.parse_args()

def Plot_Fitness_Comparison(xarray,x_title, yarray,y_title):
	""" 
		Plotting Data: 
		Input: x data, x title or x axis label , y data , y title or y axis label
	"""
	fig, ax = plt.subplots(figsize = (8, 6))

	ax.set_xlabel(x_title, fontsize = 'large')
	ax.set_ylabel(y_title, fontsize = 'large')
	# ax.set_ylim([0,710])

	for y in range(len(yarray)):
		# ax.plot(xarray, yarray[y] , markersize=4 , label = f'Configuration {indices[y]} - Tamaño de Población: {s_elit[y]}')
		ax.plot(xarray, yarray[y] , markersize=4 , label = f'Configuration {indices[y]}')
	ax.grid(True)
	ax.legend()
	plt.title(y_title + ' for different Hyperparameters Configurations')
	# plt.title(y_title + ' ' + title_plot)
	name = f"{y_title} vs {x_title} {gen}.png"
	fig.savefig(os.path.join(path_save,name))

if __name__ == '__main__':

	args = parse_args()

	# title_plot = args.plot_title
	gen = args.generation
	indices_string = args.number_files
	indices = list(map(int , indices_string.split(',')))

	path = os.path.join(os.path.dirname(__file__), 'Config_Files' )
	path_save = os.path.join(path,f'Comparing_Config_{indices_string}_gen_{gen}_Plots')
	make_dir(path_save)

	mean_values = []
	max_values= []
	gen_array=[]

	for ind in indices:
		file = os.path.join('Config_Files',f'configuration_{ind}_stats_gen_{gen}')

		file_open = open(file,'r')
		f1 = file_open.readlines()

		# Extracting Vector Columns of Generations, Mean Values, Max Values and Standard Deviation of Mean
		individual_data = [ i.split() for i in f1[2:2+gen] ]
		individual_data = np.array(individual_data).transpose()
		individual_data = [list(map(float , list_i)) for list_i in individual_data]

		# Generations Array
		if len(gen_array) == 0:
			gen_array = individual_data[0]

		# Mean Values 
		mean_values.append(individual_data[2])

		# Max Values
		max_values.append(individual_data[1])

	# Borrar Luego :
	# Parametros para la leyenda 

	# s_elit = [30,50,60,70,80,90]
	# elit = [2,5,3]


	# Plot Species Sizes vs Generation
	Plot_Fitness_Comparison(gen_array,'Generations' , mean_values, 'Fitness Mean')

	# Plot Species Fitness vs Generation
	Plot_Fitness_Comparison(gen_array,'Generations',max_values, 'Fitness Max' )
