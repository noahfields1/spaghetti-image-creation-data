import vtk
import numpy as np       
from vtk.util.numpy_support import vtk_to_numpy as v2n
from PIL import Image
import matplotlib.image
import os
path_vtk = 'results/0145_1001/Model/'
#output_path = '/home/nfields/Data/dparker/extract-2d-images/results_png/0145_1001/meshes/'
#vtiFiles= [f for f in os.listdir(path_vtk) if f.endswith('vti')]
for subdir in os.listdir(path_vtk):
    if subdir == '.DS_Store':
        continue
    blah = os.path.join(path_vtk, subdir)
    arr = [f for f in os.listdir(blah) if f.endswith('vtp')]
    for i in arr:
        print(os.path.join(blah,i))
exit()
vtpFiles= [f for f in os.listdir(path_vtk) if f.endswith('vtp')]
print(vtpFiles)
#vtiFiles = [f for f in vtiFiles if not f in os.listdir(output_path)]
#vtpFiles = [f for f in vtpFiles if not f in os.listdir(output_path)]

for vtpfile in vtpFiles:
    vtpFilePath = path_vtk + vtpfile
    vtiFilePath = path_vtk + "image" + vtpfile[5:-4] + ".vti"
    f = open(vtpFilePath, "r")
    arr = f.readlines()
    bifurcationID = int(arr[5].split()[4].split("\"")[1])
    if bifurcationID != -1:
        continue
    print(vtpfile)
    continue
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(vtiFilePath)
    reader.Update()
    vtiimage = reader.GetOutput()
    extent = vtiimage.GetExtent()
    width = extent[1] - extent[0] + 1
    height = extent[3] - extent[2] + 1
    image_data = np.reshape(v2n(vtiimage.GetPointData().GetArray(0)), (width, height))
    matplotlib.image.imsave(output_path + "image" + vtpfile[5:-4] + '.png', image_data,cmap='gray')
    img = Image.open(output_path + "image" + vtpfile[5:-4] + '.png').convert('L')
    img.save(output_path + "image" + vtpfile[5:-4] + '.png')

#print("PNGs Created")
