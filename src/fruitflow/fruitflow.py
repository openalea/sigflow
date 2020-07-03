
from math import *
from random import uniform
from random import random
import os
import numpy as np
from openalea.mtg import *
#from openalea.mtg import algo

#import openalea.plantgl.all as pgl



def compute_terminal_shoots_only(g, dist = [], alpha_fruits=0.1, alpha_leaves=0.1, half_fruits=0.1, half_leaves=0.1, shape_fruits=0.1, shape_leaves=0.1):
	whole_result_2 = {}
	g = compute_activating_inhibiting_signal_terminal_shoots_only(g, selected_scale = 2, alpha_inib = alpha_fruits, alpha_activ = alpha_leaves, dists = dist)
	g = meristem_fates(g, 2, value_at_05_fruits = half_fruits, shape_factor_fruits = shape_fruits, value_at_05_leaves = half_leaves, shape_factor_leaves = shape_leaves)
	Dict_result = {}
	#print('-------------------------------')
	for vid in g.vertices(scale = 3):
		node = g.node(vid)
		if (node.label == 'm') :
			complex_node = g.node(g.complex(vid)) 
			#print(vid, complex_node.activating)
			Dict_result[vid] = [complex_node.inhibiting,complex_node.activating, complex_node.ini_inibiting, complex_node.ini_activating, node.proba_inib, node.proba_activ, node.final_fate, complex_node.self_inhibiting, complex_node.self_activating]  
			#print Dict_result[vid]
	return Dict_result


### upscaling of leaf areas
def add_activating_and_inhibiting_signal(g) :
	"""
adds activating and inhibiting signals to an MTG

:Parameters:
- 'g' (MTG) - multi scale tree graph of the plant
        
:Returns:
An MTG 

:Remark:
- initial inhibiting signal is considered from the number of fruits on the node
- initial activating signal is calculated  by summing the node total leaf area
        
	"""
	#print('-------------------------------')
	#print('----init-')
	for vid in g.vertices(scale = 2) :
		axis_node = g.node(vid)
		axis_node.leaf_area = 0 
		axis_node.fruit_number = 0
		for cid in g.components(vid) :
			comp_node = g.node(cid)
			if (comp_node.leaf_area is not None):
				axis_node.leaf_area +=   comp_node.leaf_area
				
			if (comp_node.label == 'F'):
				axis_node.fruit_number += 1 
		axis_node.ini_inibiting = axis_node.fruit_number
		axis_node.ini_activating = axis_node.leaf_area * 10000 
		#print(vid, axis_node.ini_activating)
		axis_node.inhibiting = 0
		axis_node.activating = 0
	return(g)

def add_axis_coordinates(g,scale_):
	for vid in g.vertices(scale_):
		#print(vid)
		axis_node = g.node(vid)
		axis_node.XX, axis_node.YY, axis_node.ZZ = 0,0,0
		first_node = g.node(g.components(vid)[0])  
		last_node = g.node(g.components(vid)[len(g.components(vid))-1])
		### add a conditional if we don't have XX, YY or ZZ coordinates at some points
		axis_node.XX = (first_node.XX + last_node.XX)/2
		axis_node.YY = (first_node.YY + last_node.YY)/2
		axis_node.ZZ = (first_node.ZZ + last_node.ZZ)/2
		axis_node.length = sqrt((first_node.XX - last_node.XX)**2 + (first_node.YY + last_node.YY)**2 + (first_node.ZZ + last_node.ZZ)**2)
		axis_node.semilength = axis_node.length/2
		axis_node.base_XX = first_node.XX 
		axis_node.base_YY = first_node.YY
		axis_node.base_ZZ = first_node.ZZ
	return(g)
### upscaling of fruit number





def compute_path(g,i,j, with_gca=True):
    """
    Compute topological path between two vertices

    :Parameters:
        - 'g' (MTG) - multi scale tree graph of the plant
        - 'i', 'j' - vertices between which computing the path

    :Returns:
        topological path between verteces 'i' and 'j', excluding the two input vertices.

    :Remark:
        - When a branching point, in common between the ancestors of the vertices, is encountered, it is removed from the path.

    """


    list1 = g.Ancestors(i)
    list2 = g.Ancestors(j)

    _gca_id = algo.lowestCommonAncestor(g, [i,j])
    position1 = list1.index(_gca_id)
    position2 = list2.index(_gca_id)
    if with_gca :
        path = list1[:position1]+[_gca_id]+list(reversed(list2[:position2]))
    else :
        path = list1[:position1] + list(reversed(list2[:position2]))
    

    # uniqueAncestors = list(set(g.Ancestors(i)) ^ set(g.Ancestors(j))) #Ancestors not in common between i and j

    # if i in uniqueAncestors:
    #     uniqueAncestors.remove(i)
    # if j in uniqueAncestors:
    #     uniqueAncestors.remove(j)
    # path = uniqueAncestors
    return(path)

def compute_geometrical_distance(g,i,j):
	"""
Compute geometrical distance between two vertices based on their spatial coordinates. 
This is given by the sum of the lengths of components in the path that connects them,

:Parameters:
- 'g' (MTG) - multi scale tree graph of the plant
- 'i', 'j' - vertices between which computing the distance

:Returns:
geometrical distance between verteces 'i' and 'j', excluding the two input vertices.

	"""
	#print('------------------------')
	#print('i','j')
	#print(i,j)
	path = compute_path(g,i,j)
	if i not in path:
		path.extend([i])
	if j not in path:
		path.extend([j])
	geometrical_distance = 0
	#print('path')
	#print(path)
	for k in path :
		node = g.node(k)
		if ((k != i) or (k!=j)):
			#print('ici')
			geometrical_distance += node.length
		else:
			geometrical_distance += 0
		#print(k, node.length)
	#print(geometrical_distance)
	return(geometrical_distance)

def euclidean_distance(Xs,Ys,Zs):
    """
    Compute euclidean distance between couples of spatial coordinates by means of the pitagora theorem applied to the X, Y, Z coordinates.

    :Parameters:
        - 'Xs, Ys, Zs' - couples of x,y,z spatial coordinates

    :Returns:
        euclidean distance between the points defined by the X,Y,Z couples of spatial coordinates
    """
    import math
    #print Xs, Ys, Zs
    euclidean_distance = math.sqrt((Xs[0] - Xs[1])**2 + (Ys[0] - Ys[1])**2 + (Zs[0] - Zs[1])**2)
    return(euclidean_distance)

def compute_distance_B(g, i, j):
    distance = 0
    path = compute_path(g,i,j, False)
    
    for k in range(0, len(path)-1) :
        f_node = g.node(path[k])
        s_node = g.node(path[k+1])
        # print path[k]
        # print f_node.base_XX , f_node.base_YY, f_node.base_ZZ
        # print path[k+1]
        # print s_node.base_XX , s_node.base_YY, s_node.base_ZZ
        # print euclidean_distance([f_node.base_XX,s_node.base_XX],[f_node.base_YY,s_node.base_YY],[f_node.base_ZZ,s_node.base_ZZ])
        # print str('----------------------------------------------------')
        distance += euclidean_distance([f_node.base_XX,s_node.base_XX],[f_node.base_YY,s_node.base_YY],[f_node.base_ZZ,s_node.base_ZZ])
    return(distance)   

class DistanceMatrix(object):
    def __init__(self, vtxlist):
        self.idmap = dict([(vid,i) for i,vid in enumerate(vtxlist)])
        size = len(vtxlist)
        self.values = np.zeros((size, size))

    def __getitem__(self, vids):
        v1, v2 = vids
        return self.values[self.idmap[v1]][self.idmap[v2]]

    def __setitem__(self, vids, value ):
        v1, v2 = vids
        self.values[self.idmap[v1]][self.idmap[v2]] = value

def compute_distance_matrix(g,selected_scale): 
	"""
Computes a matrix of distances between vertices at scale 'selected_scale'

:Parameters:
- 'g' (MTG) - multi scale tree graph of the plant
- 'selected_scale' (int) - topological scale of the tree components between which computing distances

:Returns:
- Dists - a matrix of distances

	"""
	ax_terms = [aid for aid in g.vertices(selected_scale) if g.node(aid).nb_children() == 0]

	dists = DistanceMatrix(ax_terms)
	for i in ax_terms:
		for j in ax_terms:
            # dists[Leaf,Demand] = compute_geometrical_distance(g,Leaf,Demand, selected_scale)                # substituted to be able to have distance from component to same component = 0
			#print('i','j')
			if j > i:
				dists[i,j] = compute_distance_B(g,i,j)
			else:
				dists[i,j] = dists[j,i]

	return(dists)

	


def compute_activating_inhibiting_signal_terminal_shoots_only(g, selected_scale, alpha_inib, alpha_activ, dists):
	
 	ax_terms = [aid for aid in g.vertices(selected_scale) if g.node(aid).nb_children() == 0]
	print(ax_terms)
	#Tot_inhibiting = 0
	#Tot_ini_inhibiting = 0
	#Tot_activating = 0
	#Tot_ini_activating = 0 
	
	# for vid in g.vertices(selected_scale):
	# 	node = g.node(vid)
	# 	node.inibiting = 0
	# 	node.activating = 0
	# 	#Tot_ini_inhibiting += node.ini_inibiting
	# 	Tot_ini_activating += node.ini_activating
	
	#print('fonction_axis')
	#factor_shoot = 24fr/44pousses=0.52	
	#factor_branch = 27fr/45pousses=0.6
	factor = 1 ###0.86
	for vid in ax_terms:
		print("---------")
		print(vid)
		node = g.node(vid)
		node.tot_inhibiting = 0
		node.tot_activating = 0
		#node.inibiting = 0
		#node.activating = 0

		for jid in ax_terms:
			match_node = g.node(jid)
			match_node.current_inhibiting = node.ini_inibiting * (1 / (1+dists[vid,jid]))**alpha_inib
			match_node.current_activating = node.ini_activating * 10000 * (1 / (1+dists[vid,jid]))**alpha_activ 
			#print('-------------------------------')
			#print('----ini_activating-')
			#print(vid, node.ini_activating)
			if jid == vid :
				node.self_inhibiting = match_node.current_inhibiting
				node.self_activating = match_node.current_activating
			node.tot_inhibiting += match_node.current_inhibiting
			node.tot_activating += match_node.current_activating

		for jid in ax_terms:
			match_node = g.node(jid)
			if (node.ini_inibiting != 0) :
				match_node.inhibiting +=  match_node.current_inhibiting  * node.ini_inibiting / node.tot_inhibiting * factor
				node.self_inhibiting = node.self_inhibiting * node.ini_inibiting / node.tot_inhibiting
			if (node.ini_activating !=0) :
				match_node.activating += match_node.current_activating * node.ini_activating / node.tot_activating	* factor
				node.self_activating = node.self_activating * node.ini_activating / node.tot_activating
	
	return(g)


def meristem_fates(g, selected_scale, value_at_05_fruits =0.5, shape_factor_fruits =0.5, value_at_05_leaves = 2, shape_factor_leaves = 2):
	"""
gives the meristems fates 

:Parameters:
- 'g' (MTG) - multi scale tree graph of the plant
- 'selected_scale' (int) - topological scale of the tree components 
- value_at_05_fruits -   
- shape_factor_fruits -   
- value_at_05_leaves -   
- shape_factor_leaves -   
        
:Returns:
an MTG with attributes
'inibiting' - inhibiting signal available for a component,
'activating' - activating signal available for a component,
'fruit_fate' - meristem fate for the computed inhibition signal, 
'leaf_fate' - meristem fate for  the computed activation signal,
'proba_inib' - probability of inhibition,
'proba_activ' - probability of activation   
   
	"""
	#print('-------------------------------')
	#print('----proba-')
	for vid in g.vertices(selected_scale + 1):
		if (g.node(vid).label == 'm') : 
			#g.node(vid).fruit_fate, g.node(vid).proba_inib = compute_fate_fruit_2(g.node(g.complex(vid)).inhibiting, value_at_05_fruits)
			#g.node(vid).leaf_fate, g.node(vid).proba_activ  =  compute_fate_leaf_2(g.node(g.complex(vid)).activating, value_at_05_leaves)
			g.node(vid).fruit_fate, g.node(vid).proba_inib = compute_fate_fruit(g.node(g.complex(vid)).inhibiting, value_at_05_fruits, shape_factor_fruits)
			g.node(vid).leaf_fate, g.node(vid).proba_activ  =  compute_fate_leaf(g.node(g.complex(vid)).activating, value_at_05_leaves, shape_factor_leaves)
			#print(vid, g.node(g.complex(vid)).activating)
			#print(g.node(g.complex(vid)).activating)
			g.node(vid).final_fate = (1-g.node(vid).proba_inib)* g.node(vid).proba_activ
			#print(g.node(vid).fruit_fate, g.node(vid).proba_inib, g.node(g.complex(vid)).inhibiting, shape_factor_fruits)
	#print io.write_mtg(g, [('inibiting', 'REAL'), ('activating', 'REAL'), ('fruit_fate', 'ALPHA'), ('leaf_fate', 'ALPHA'), ('proba_inib', 'REAL'),('proba_activ','REAL'), ('final_fate', 'REAL')])
	return g


def probability_value(x,b=0.5,c=0.5):
	#print([x,b,c])
	return (1 / (1 + exp(-(x-b)/c)))

def compute_fate_fruit(inhiting_signal, value_at_05, shape_factor):
	if (uniform(0,1) < probability_value(inhiting_signal, value_at_05,shape_factor)) :
		fate = "inhibited"
	else :
		fate = "activated"
	return fate, probability_value(inhiting_signal, value_at_05,shape_factor)

def compute_fate_leaf(inhiting_signal, value_at_05, shape_factor):
	if (uniform(0,1) > probability_value(inhiting_signal, value_at_05,shape_factor)) :
		fate = "inhibited"
	else :
		fate = "activated"
	return fate , probability_value(inhiting_signal, value_at_05,shape_factor)

def compute_fate_fruit_2(inhiting_signal, value_at_05):
	if inhiting_signal > value_at_05 :
		return "inhibited", 1
	else :
		return "activated", 0

def compute_fate_leaf_2(inhiting_signal, value_at_05):
	if inhiting_signal < value_at_05 :
		return "inhibited", 0
	else :
		return "activated", 1