#!/bin/bash
model=$1
#images_path=ls $model/Images/*.vti
#meshes_path=ls $model/Meshes/*.vtp
#models_path=ls $model/Models/*.vtp
search_dir=./$model/Paths/
mkdir ./3D_points
mkdir ./3D_points/$model
mkdir ./2D_points/
mkdir ./2D_points/$model
mkdir ./2D_points_clean/
mkdir ./2D_points_clean/$model
mkdir ./files/
mkdir ./files/$model
mkdir ./results
mkdir ./results/$model
mkdir ./results/$model/Model
mkdir ./results/$model/Mesh
for path_dir in $search_dir*
do
	#echo $model
	path_name=${path_dir#"$search_dir"}
	path_name=${path_name%".pth"}
	mkdir ./2D_points_clean/$model/$path_name
	mkdir ./files/$model/$path_name
	mkdir ./3D_points/$model/$path_name
	mkdir ./2D_points/$model/$path_name
	mkdir ./results/$model/Model/$path_name
	mkdir ./results/$model/Mesh/$path_name
	python3 extract-2d-images.py --image-file $model/Images/OSMSC${model:0:4}-cm.vti --path-file $path_dir --model-file $model/Models/$model.vtp --slice-increment 10 --path-sample-method number --slice-width 5 --extract-slices true --results-directory ./results/$model/Model/$path_name

	python3 extract-2d-images.py --image-file $model/Images/OSMSC${model:0:4}-cm.vti --path-file $path_dir --model-file $model/Meshes/$model.vtp --slice-increment 10 --path-sample-method number --slice-width 5 --extract-slices true --results-directory ./results/$model/Mesh/$path_name


done

find ./3D_points -name "*.txt" -type f -size -500c -delete
find . -name "*.DS_Store" -type f -delete

#python3 create_labels.py
#python3 filter_vessels.py
