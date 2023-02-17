import tools
import numpy as np

vtp = tools.read_geo('/Users/noah/Desktop/extract-2d-images/results/0083_2002/Model/LPA/model_slice_30.vtp')
#vtp = tools.read_geo('/Users/noah/Downloads/0145_1001.vtp')
#res = tools.collect_arrays(vtp)
#print(res)
#print(vtp)
point_data, _, points = tools.get_all_arrays(vtp.GetOutput())
print(point_data.keys())
#bifurcationId = point_data['BifurcationId']
#print(np.sum(bifurcationId),len(bifurcationId))

for i in point_data.keys():
	print(str(i) + " " + str(point_data[i]))
#print(point_data['CenterlineSectionShape'])
def get_bifurcationID(vtp_file):
	vtp = tools.read_geo(vtp_file)
	point_data, _, points = tools.get_all_arrays(vtp.GetOutput())
	bifurcationId = point_data['BifurcationId']
	return bifurcationId
