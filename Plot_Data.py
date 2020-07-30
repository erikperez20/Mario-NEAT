#######################################################################
######################     Plotting Data     ##########################
#######################################################################


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

	parser = argparse.ArgumentParser('Visualize your data statistics')
	parser.add_argument('--stats_file', type = str , help = 'Statistics File for Visualization')

	return parser.parse_args()

def Plot_Fitness_vs_Generation(xarray,x_title,yarray,y_title):

	""" 
		Plotting Data: 

		Input: x data, x title or x axis label , y data , y title or y axis label

	"""

	fig, ax = plt.subplots(figsize = (8, 6))
	ax.set_xlabel(x_title, fontsize = 'large')
	ax.set_ylabel(y_title, fontsize = 'large')
	# ax.set_xticks(xarray)
	# ax.set_yticks(yarray)
	# ax.tick_params(direction = 'in')
	ax.plot(xarray, yarray , markersize=4 )
	ax.grid(True)
	plt.title(y_title + ' vs ' + x_title)
	name = f"{y_title} vs {x_title} {gen}.png"
	fig.savefig(os.path.join(file_path,name))
	# plt.show()


def Plot_Species_vs_Generation(xarray,x_title, yarray,y_title):

	""" 
		Plotting Data: 

		Input: x data, x title or x axis label , y data , y title or y axis label

	"""
	fig, ax = plt.subplots(figsize = (8, 6))

	ax.set_xlabel(x_title, fontsize = 'large')
	ax.set_ylabel(y_title, fontsize = 'large')
	# ax.set_xticks(xarray)
	# ax.set_yticks(yarray[0])
	# ax.tick_params(direction = 'in')
	for y in range(len(yarray)):
		ax.plot(xarray, yarray[y] , markersize=4 , label = f'Species {y+1}')

	ax.grid(True)
	ax.legend()
	plt.title(y_title + ' vs ' + x_title)
	name = f"{y_title} vs {x_title} {gen}.png"
	fig.savefig(os.path.join(file_path,name))
	# plt.show()


if __name__ == "__main__":

	args = parse_args()
	filename = args.stats_file
	path = os.path.dirname(__file__)
	print(path)
	file_path = os.path.join(path,filename+'_Plots')
	make_dir(file_path)
	gen = int(filename.split('_')[-1])
	print(gen)

	file = open(filename, 'r')
	f1 = file.readlines()

	##################################
	# Generations = individual_dat[0]
	# Max : individual_data[1]
	# Mean: individual_data[2]
	# Std: individual_data[3]
	##################################

	individual_data = [ i.split() for i in f1[2:2+gen] ]
	individual_data = np.array(individual_data).transpose()
	individual_data = [list(map(float , list_i)) for list_i in individual_data]

	##################################
	# Generations = species_size_data[0] = species_fit_data[0]
	# Species (i) Size : species_sizes[i]
	# Species (i) Fitness: species_fit[i]

	##################################

	species_size_data = [i.split() for i in f1[5+gen: 5 + 2*gen ]]
	species_size_data = np.array(species_size_data).transpose()
	species_size_data = [list(map(float , list_i)) for list_i in species_size_data]
	species_sizes = species_size_data[1:]


	species_fit_data = [i.split() for i in f1[7 + 2*gen : ]]
	species_fit_data = np.array(species_fit_data).transpose()
	species_fit_data = [ [float(i) if i != 'NA' else 0  for i in list_i] for list_i in species_fit_data ]
	species_fit = species_fit_data[1:]

	# Plot Fitness Mean vs Generation
	Plot_Fitness_vs_Generation(individual_data[0],'Generations',individual_data[2], 'Fitness Mean')

	# Plot Fitness Max vs Generation
	Plot_Fitness_vs_Generation(individual_data[0],'Generations',individual_data[1], 'Fitness Max')

	# Plot Species Sizes vs Generation
	Plot_Species_vs_Generation(species_size_data[0],'Generations' , species_sizes, 'Species Sizes')

	# Plot Species Fitness vs Generation
	Plot_Species_vs_Generation(species_fit_data[0],'Generations', species_fit, 'Species Mean Fitness' )





