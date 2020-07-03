

import time
from .fruitflow import * 


def run_all_mtg(file_name):
	list_of_mtgs = os.listdir(os.path.join(os.getcwd() , 'fruit_removal'))
	for i in list_of_mtgs :
		run_simulation(file_name, i) 

def run_simulation(mtg_name, directory, alpha_fruit_=2.3, alpha_leaves_=4.5, value_at_50_fruit_= 0.70, values_at_50_leaves_=40.4
	, shape_fruit_=0.25, shape_leaves_ = 20): 
	print("alpha_leaves")
	print(alpha_leaves_)
	whole_dict_result = {}
	#mtg_file = os.getcwd() + '\\' + mtg_name
	mtg_file = directory + '\\architectures\\' + mtg_name
	g = MTG(mtg_file)
	g = add_axis_coordinates(g,2)
	print('computing_distance_matrix')
	start_time_2 = time.time()
	dists= compute_distance_matrix(g,2)
	print('distance_matrix_computed')
	print('duration_for_compute_distances')
	print(time.time() - start_time_2)
	g = add_activating_and_inhibiting_signal(g)
	result = compute_terminal_shoots_only(g, dists, alpha_fruit_, alpha_leaves_, value_at_50_fruit_, values_at_50_leaves_, shape_fruit_, shape_leaves_)
	whole_dict_result[0] = result
	write_results(mtg_name, whole_dict_result)
	return g,dists, whole_dict_result

	



def run_multiple_simulation(mtg_name, file_name, directory): 

	path = directory + '\\share\\' +   file_name
	mtg_file = directory + '\\architectures\\' + mtg_name
	g = MTG(mtg_file)
	complete_file = np.genfromtxt(path, names=True, delimiter='\t', dtype=None)
	
	g = add_axis_coordinates(g,2)
	print('computing_distance_matrix')
	start_time_2 = time.time()
	dists= compute_distance_matrix(g,2)
	print('distance_matrix_computed')
	print('duration_for_compute_distances')
	print(time.time() - start_time_2)
	whole_dict_result = {}

	for i in range(0,(len(complete_file))):
		#print(complete_file[i])
		alpha_fruits =  complete_file[i]['alpha_inhib']
		alpha_leaves = complete_file[i]['alpha_activ']
		half_fruits = complete_file[i]['value_at_50_fruit']
		half_leaves = complete_file[i]['value_at_50_leaves'] #90
		shape_fruits = complete_file[i]['shape_fruit']  ### 0.25
		print("shape fruits")
		print(shape_fruits)
		shape_leaves = complete_file[i]['shape_leaves'] ##200
		print("shape_leaves")
		print(shape_leaves)
		g = add_activating_and_inhibiting_signal(g)
		result = compute_terminal_shoots_only(g, dists, alpha_fruits, alpha_leaves, half_fruits, half_leaves, shape_fruits, shape_leaves)
		
		whole_dict_result[i] = result
	#print(whole_dict_result)
	write_results(mtg_name, whole_dict_result)
	return g,dists, whole_dict_result
	
	
def write_results(mtg_name, dict_result):
	filename = 'result_' +  mtg_name +  '.txt'
	
	if not os.path.exists('simulation_results'):
		#print(complete_file[i])
		os.mkdir('simulation_results')

	filename = os.getcwd() +  '\\simulation_results' + '\\' + filename

	file = open(filename,'w')  
	file.write("simulation" + "\t" + "meristem" +  "\t" + "inhibiting" + "\t" +  "activating" + "\t" + "number of fruits" + "\t" +  "Leaf area" + "\t"+  "inhibition proba" + "\t"+  "activation proba" +  "\t"+  "final_proba" + "\t" +  "self.inhibiting" + "\t" + "self.activating" + "\n")
	for key in dict_result:
		dict_simu = dict_result[key]
		for key_simu in dict_simu:
			file.write(str(key) +  "\t" + str(key_simu) +  "\t" + str(dict_simu[key_simu][0]) + "\t" +  str(dict_simu[key_simu][1]) + "\t" +  str(dict_simu[key_simu][2]) +"\t" +   str(dict_simu[key_simu][3]) + "\t" +  str(dict_simu[key_simu][4]) + "\t" +  str(dict_simu[key_simu][5])+ "\t" +  str(dict_simu[key_simu][6])+ "\t" +  str(dict_simu[key_simu][7]) + "\t" +  str(dict_simu[key_simu][8]) + "\n") 
	file.close()

