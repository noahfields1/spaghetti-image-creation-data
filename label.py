import matplotlib.pyplot as plt
import numpy as np
import math
from PIL import Image
import os

def middle(arr):
	for i in arr:
		x += arr[0]
		y += arr[1]
	x = x / len(arr)
	y = y / len(arr)
	return x,y


def neighbors(p1,p2):
	x_true = True
	y_true = True
	if abs(p1[0]-p2[0]) > 1:
		x_true = False
	if abs(p1[1]-p2[1]) > 1:
		y_true = False
	return x_true and y_true

def createIMG(path):
	arr = np.zeros((240,240))
	f = open(path,'r')
	originals = set()
	for i in f.readlines():
		point = i.rstrip().split()
		if int(float(point[0])) >= 240 or int(float(point[1])) >= 240:
			continue
		if int(float(point[0])) < 0 or int(float(point[1])) < 0:
			continue
		originals.add((int(float(point[0])),int(float(point[1]))))
		arr[int(float(point[0])),int(float(point[1]))] = 1

	if np.sum(arr) == 0:
		return
	arr = arr * 255
	arr = arr.astype(np.uint8)
	im = Image.fromarray(arr)
	if 'clean' in path:
		im_path = path.replace('2D_points_clean_','')
		im_path = im_path.replace('txt','Yc.png')
		im_path = im_path.replace('2D_points_clean','files')
		im.save(im_path)
		np_path = im_path.replace('png','npy')
		np.save(np_path,arr)
	else:
		im_path = path.replace('2D_points_','')
		im_path = im_path.replace('txt','Y.png')
		im_path = im_path.replace('2D_points','files')
		im.save(im_path)

def connectPts(path_2D,path_2D_clean):
	#Reading in the points from 'path_2D'
	f = open(path_2D,'r')
	points = []
	points_set = set()
	for i in f.readlines():
		point = i.rstrip().split()
		points.append((int(float(point[0])),int(float(point[1]))))
		points_set.add((int(float(point[0])),int(float(point[1]))))
	points = list(points_set)
	f.close()
	#If there are no points (or just the origin), we get rid of the point
	#This is the case when a pathway point is created without a segmentation
	if len(points) <= 1:
		return
	#The origin is the first point (also known as the centerpoint of the pathway)
	origin = (121,121)
	min = 10000
	min_index = None

	#Find the closest point to the centerpoint of the pathway (origin)
	for i in range(0,len(points)):
		dist_from_origin = ((origin[0] - points[i][0])**2 + (origin[1] - points[i][1])**2)**0.5
		if dist_from_origin < min:
			min = dist_from_origin
			min_index = i
	first_point = points.pop(min_index)

	#Finding all the points in the vessels
	#points is the array of all the points, and we are selectively adding points to vessel array
	old_point = first_point
	next_point = None
	next_point_index = None
	old_tangent = None
	new_tangent = None
	min = 10000
	vessel = []
	while next_point != first_point and len(points) != 0:
		min = 10000
		next_point_index = None
		for i in range(0,len(points)):
			dist_from_old_point = ((old_point[0] - points[i][0])**2 + (old_point[1] - points[i][1])**2)**0.5
			if dist_from_old_point < min:
				min = dist_from_old_point
				next_point_index = i
		next_point = points[next_point_index]
		old_point = points.pop(next_point_index)
		vessel.append(old_point)
		if len(vessel) == 10:
			points.append(first_point)

	#add the first point back again, so we have a complete circle
	vessel.append(vessel[0])
	
	#Recursively go through all of the points and add the midpoints to the vessels
	#until all of the points are connected
	finished = False
	i = 0
	while not finished:
		if not neighbors(vessel[i],vessel[i+1]):
			x_mid = round((vessel[i][0] + vessel[i+1][0])/2)
			y_mid = round((vessel[i][1] + vessel[i+1][1])/2)
			midpoint = (x_mid,y_mid)
			vessel.insert(i+1,midpoint)
			i = i - 1
		i += 1
		if i == len(vessel)-1:
			finished = True

	start = [(121,121)]
	used = set(vessel)

	while len(start) != 0:
		next = start.pop(0)
		if next in used:
			continue
		if next[1] == 239 or next[1] == 0 or next[0] == 0 or next[0] == 239:
			used.add(next)
			return
		used.add(next)
		if (next[0]+1,next[1]) not in used:
			start.append((next[0]+1,next[1]))
		if (next[0],next[1]+1) not in used:
			start.append((next[0],next[1]+1))
		if (next[0]-1,next[1]) not in used:
			start.append((next[0]-1,next[1]))
		if (next[0],next[1]-1) not in used:
			start.append((next[0],next[1]-1))
	used.add((121,121))
	
	if len(used) > 40000:
		return
	vessel = used
	f = open(path_2D_clean,'w')
	for i in vessel:
		f.write(str(i[0]) + '\t' + str(i[1]) + '\n')
	f.close()
