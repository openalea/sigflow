
from builtins import str
from openalea.plantgl import scenegraph as pglsc
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
from openalea.plantgl import gui as pglgui
from openalea.plantgl.all import *
from openalea.mtg import plantframe, io 
from .simulation import *



def update_mtg(g, mtg_name, dict_results, directory, sim_id=0):
	g.add_property('inhibiting')
	g.add_property('activating')
	g.add_property('final.proba')
	res = dict_results[sim_id]
	for vid, data in list(res.items()):
		n = g.node(vid)
  		n.inhibiting = data[0]
		n.activating = data[1]
		n.final_proba = data[6]
	
	variable_list = [("TopDia","REAL"),("XX","REAL"),("YY","REAL"),("ZZ","REAL"),("AA","REAL"),("BB","REAL"),("CC","REAL"),("leaf_area","REAL"),("inhibiting","REAL"), ("activating", "REAL"), ("final_proba", "REAL")]
	output_file_name = str(mtg_name.split(".")[0] + "_sim" + ".mtg")
	filename = directory +  '\\simulation_results' + '\\' + output_file_name
	l= open(filename,"w")
	l.write(io.write_mtg(g,variable_list))
	l.close()		



	return(g)



def create_scene(g):
 xmin = 999999
 xmax = -999999
 ymin = 999999
 ymax = -999999
 zmin = 999999
 zmax = -999999
 for vid in g.vertices(scale=3):
 	xmin = min(xmin, g.node(vid).XX)
 	xmax = max(xmax, g.node(vid).XX)
 	ymin = min(ymin, g.node(vid).YY)
 	ymax = max(ymax, g.node(vid).YY)
 	zmin = min(zmin, g.node(vid).ZZ)
 	zmax = max(zmax, g.node(vid).ZZ)

 unit = 10
  
 dressing_data = plantframe.DressingData(DiameterUnit=unit)
 pf = plantframe.PlantFrame(g, TopDiameter='TopDia', DressingData=dressing_data)
 scn = pf.plot(gc=True)
 return(scn)



def extract_mtg_visu(g,mtg_name, dict_results, directory, sim_id = 0):
 
 #mtg_file = directory + '\\architectures\\' + mtg_name
 g = update_mtg(g, mtg_name,dict_results, directory, sim_id)
 scn = create_scene(g)
 matM =pglsc.Material((0, 255, 0))
 matF =pglsc.Material((213,231,81))
 matm =pglsc.Material((0, 0, 255))
 mcm = cm.get_cmap('jet')
 cmap = LinearSegmentedColormap.from_list('name', ['red', 'blue'])
  
 acc = 0 
 for vid in g.vertices(scale=3):
  acc += 1 
  n = g.node(vid)
  if n.label.startswith("M"):
   pos = (n.XX, n.YY, n.ZZ)
   if n.leaf_area != 0 :
	sca = np.sqrt(n.leaf_area / 0.00353284)
	ll = 0.11
	lw=0.027
	points = [(0,-lw,0.03),
	(ll,-lw,0.03),
	(ll,0,0),
	(ll,lw,0.03),
	(0,lw,0.03),
	(0,0,0)]
	# list of indices
	indices = [(0, 1, 2, 5), (2,3,4,5)]
	# creating the geometry
	leaf = QuadSet(points,indices)
	# creating a texture from a file
	tex = ImageTexture("./apple-leaf.png")
	# the coordinates of the texture that we may use
	texCoord = [(0,0),(1,0),(1,0.5),(1,1),(0,1),(0,0.5)]
	# how we associate the coordinates of the texture to
	# the vertices of the quad
	texCoordIndices = [(0,1,2,5),(2,3,4,5)]
	# adding those informations to the geometry
	leaf.texCoordList = texCoord
	leaf.texCoordIndexList = texCoordIndices
	from math import pi
	leaf = pglsc.Scaled(sca, sca, sca,leaf)
	angle = random.randrange(0,70,15)
	leaf = pglsc.AxisRotated((0,1,0),radians(angle),leaf)
	leaf = pglsc.AxisRotated((0,0,1),radians(acc*140), leaf)
	import openalea.plantgl.all as pgl
	geom = pglsc.Translated(pos, leaf)  # unit conversion for plantgl
	scn.add(pglsc.Shape(geom, tex))
  elif n.label.startswith("F"):
   pos = (n.XX, n.YY, n.ZZ)
   geom = pglsc.Translated(pos, pglsc.Sphere(0.03))  # unit conversion for plantgl
   scn.add(pglsc.Shape(geom, matF))
  elif n.label.startswith("m"):
   pos = (n.XX, n.YY, n.ZZ)
   geom = pglsc.Translated(pos, pglsc.Sphere(0.010))  # unit conversion for plantgl
   #mat = pglsc.Material([int(v * 255) for v in mcm(int(n.inhibiting * 255))[:3]])
   mat = pglsc.Material([int(v * 255) for v in cmap(int(n.final_proba * 255))[:3]])
   scn.add(pglsc.Shape(geom, mat))
 #return(scene)
 pglgui.Viewer.display(scn)
	



