#--------- FIRST BLOCKS, FIXED
print("""
[DEFAULT]
cores=4

#the base where all the input data is stored
infolder=/home/nelson/research/paper-drone2report/case_studies/case-study-5_image_classification/

#the folder for all the output of the computation (subfolders will be 
#created)
outfolder=${DEFAULT:infolder}/results

#if this field is set to True no result will be overwritten: if a result
#of a specific analysis is already present (due to previous runs) that
#analysis will be skipped altogether 
skip_if_already_done=True

#some methods support a more verbose interface, printing info and warning messages
verbose=True

[TASK classify_resnet]
active=True
model=${DEFAULT:infolder}/resnet50_final_notest.keras
#these are the human readable labels
labels = ["broadleaf", "grass", "soil", "soybean"]
#this is the input shape of the network
input_size_width = 224
input_size_height = 224
#where to save
outfile=${DEFAULT:outfolder}/resnet50_predictions.csv
verbose=True
""")

#--------- VARIOUS DATA BLOCKS, ONE PER IMAGE
example = """
[DATA broadleaf]
active=True
type=tif_multichannel
orthomosaic=${DEFAULT:infolder}/weed-detection-in-soybean-crops/grass/2.tif
channels=Red,Green,Blue
visible_channels=Red,Green,Blue
shapes_file=${DEFAULT:infolder}/weed-detection-in-soybean-crops/grass/2.shp
shapes_index=gid
"""
labels = ["broadleaf", "grass", "soil", "soybean"]

for i in range(10):
	for lab in labels:
		print('[DATA ' + lab + '_' + str(i+1) + ']')
		print('active=True')
		print('type=tif_multichannel')
		print('orthomosaic=${DEFAULT:infolder}/weed-detection-in-soybean-crops/' + lab + '/' + str(i+1) + '.tif')
		print('channels=Red,Green,Blue')
		print('visible_channels=Red,Green,Blue')
		print('shapes_file=${DEFAULT:infolder}/weed-detection-in-soybean-crops/' + lab + '/' + str(i+1) + '.shp')
		print('shapes_index=gid')
		print('')
		
