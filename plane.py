import numpy as np
import math
import matplotlib.pyplot as plt


def dist(p1,p2):
	dist = (p2[0]-p1[0]) **2 + (p2[1]-p1[1]) **2 + (p2[2]-p1[2]) **2
	return dist ** 0.5
def neighbors(p1,p2):
	x_true = True
	y_true = True
	if abs(p1[0]-p2[0]) > 1:
		x_true = False
	if abs(p1[1]-p2[1]) > 1:
		y_true = False
	return x_true and y_true

def make2Dpoints(path):
	filename = open(path,'r')
	pts = []
	x_min = 10000
	y_min = 10000
	x_max = -10000
	y_max = -10000
	for line in filename.readlines():
		coord = line.split()
		x = (float(coord[0]))
		y = (float(coord[1]))
		z = (float(coord[2]))
		pts.append(np.array([x,y,z]))
	new_origin = pts[0]
	for i in range(len(pts)):
		pts[i] = pts[i] - new_origin
	#print(pts[0],pts[1],pts[2],pts[3])
	vec1 = pts[1] - pts[0]
	vec2 = pts[2] - pts[0]
	vec3 = pts[3] - pts[0]
	new_pts = []
	for i in pts:
		a = (np.dot(i,vec1)/np.dot(vec1,vec1)) * 240
		b = (np.dot(i,vec3)/np.dot(vec3,vec3)) * 240
		new_pts.append((a,b))
	new_pts = new_pts[4:]
	path_2d = path.replace('3D_points','2D_points')
	f = open(path_2d,'w')
	
	for i in new_pts:
		f.write(str(i[0]) + '\t' + str(i[1]) + '\n')
	f.close()
