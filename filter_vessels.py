import vtk
import numpy as np       
from vtk.util.numpy_support import vtk_to_numpy as v2n
from PIL import Image
import matplotlib.image
import os
import yaml
import play
path_vtk = 'results/0083_2002/Model/'
vtpFiles = []
files_path = './files_new.txt'
file_list = open(files_path,'w')
for subdir in os.listdir(path_vtk):
    if subdir == '.DS_Store':
        continue
    blah = os.path.join(path_vtk, subdir)
    arr = [f for f in os.listdir(blah) if f.endswith('vtp')]
    for i in arr:
        vtpFiles.append(os.path.join(blah,i))

for vtpfile in vtpFiles:
	f = open(vtpfile, "r")
	arr = f.readlines()
	bifurcationID = play.get_bifurcationID(vtpfile)
	Yc_file = vtpfile.replace('results','files').replace('Model/','').replace('model_slice_','').replace('vtp','Yc.png')
	if bifurcationID != -1 or not os.path.isfile(Yc_file):
		points3D_file = vtpfile.replace('results','3D_points')
		points3D_file = points3D_file.replace('model_slice','3D_points')
		points3D_file = points3D_file.replace('vtp','txt')
		points3D_file = points3D_file.replace('Model/','')
		if os.path.isfile(points3D_file):
			os.remove(points3D_file)
		continue
	#print(Yc_file)
	Y_file = Yc_file.replace('Yc','Y')

	vtiFile_path = vtpfile.replace('model','image')
	vtiFile_path = vtiFile_path.replace('vtp','vti')
	reader = vtk.vtkXMLImageDataReader()	
	reader.SetFileName(vtiFile_path)
	reader.Update()
	vtiimage = reader.GetOutput()
	extent = vtiimage.GetExtent()
	width = extent[1] - extent[0] + 1
	height = extent[3] - extent[2] + 1
	image_data = np.reshape(v2n(vtiimage.GetPointData().GetArray(0)), (width, height))
	matplotlib.image.imsave('temp.png', image_data,cmap='gray')
	img = Image.open('temp.png').convert('L')
	X_path = vtpfile.replace('results','files')
	X_path = X_path.replace('model_slice_','')
	X_path = X_path.replace('vtp','X.png')
	X_path = X_path.replace('Model/','')
	X_np_path = X_path.replace('png','npy')
	np.save(X_np_path,image_data)
	img.save(X_path)

	arr = X_path.split('/')
	image_path = arr[1]
	path_name = arr[2]
	Y_path = X_path.replace('X','Y')
	Yc_path = X_path.replace('X','Yc')
	point = int(arr[-1].split('.')[0])
	yaml_file = X_path.replace('X.','')
	yaml_file = yaml_file.replace('png','yaml')
	file_list.write(yaml_file + '\n')
	yaml_dict = [{'X':X_np_path},{'Y':Y_path.replace('png','npy')},{'Yc':Yc_path.replace('png','npy')},{'dimensions':160},{'extent':240},{'image':image_path},{'path_id':''},{'path_name':path_name},{'point':point},{'radius':''},{'spacing':''}]
	with open(yaml_file, 'w') as file:
		documents = yaml.dump(yaml_dict,file)
