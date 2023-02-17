import label
import plane as plane
import os


dir = "/Users/noah/Desktop/extract-2d-images/3D_points"

for patient in os.listdir(dir):
	#if patient == "0083_2002":
		#continue
	for path in os.listdir(dir + '/' + patient):
		for filename in os.listdir(dir + '/' + patient + '/' + path):
			path_name = dir + '/' + patient + '/' + path + '/' + filename
			print(path_name)
			point_id = int(path_name.split('/')[-1].split('_')[2][:-4])
			plane.make2Dpoints(path_name)
			path_2D = path_name.replace('3D','2D')
			path_2D_clean = path_2D.replace('2D_points','2D_points_clean')
			label.connectPts(path_2D,path_2D_clean)
			label.createIMG(path_2D)
			if not os.path.isfile(path_2D_clean):
				continue
			label.createIMG(path_2D_clean)
			#exit()
