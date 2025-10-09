Repository for code and data used for the software article on [drone2report](https://github.com/ne1s0n/drone2report), to be submitted to [Plant Methods](https://plantmethods.biomedcentral.com/).
This work is partly supported by the research project [Polyploidbreeding](https://polyploidbreeding.ibba.cnr.it/).

### Data

- [TODO]: description of data
- [TODO]: prepare clean config.ini files to reproduce the different examples

### Case study n. 1 - thresholding

#### Tobacco leaves

1. Calculate GLI index values for each pixel of the tobacco leaves RGB image. We use the following `python` script specifying the project folder (`--base_folder`), the target folder for results (`--target_dir`), the name of the image file to be processed (`fname`), the vegetation index that we want to calculate (`--vix`), and the channels in the image (`--chan`): 


`python scripts/get_index_values.py --base_folder </path/to/my/project/folder> --target_dir </path/to/results/folder> --fname data/tobacco_leaves/tobacco_leaves.tif --vix GLI --chan 'red,green,blue'`

2. Apply threshold to remove background noise and calculate the GLI index only on tobacco leaves. You will use `drone2report` (from https://github.com/ne1s0n/drone2report) with the configuration file [RGB_tobacco_leaves_GLI.ini](case_studies/case-study-1/RGB_tobacco_leaves_GLI.ini) 

`python drone2report/drone2report.py paper-drone2report/support_material/RGB_tobacco_leaves_GLI.ini`

3. Produce a thumbnail of the tobacco leaves image with threshold on GLI > 0.1. Use [drone2report](https://github.com/ne1s0n/drone2report) with the configuration file [RGB_tobacco_leaves_thumbnails.ini](case_studies/case-study-1/RGB_tobacco_leaves_thumbnails.ini) 

`python drone2report/drone2report.py paper-drone2report/support_material/RGB_tobacco_leaves_thumbnails.ini`

#### Barley field

### Case study n. 2 - monitoring vegetation indices over time
