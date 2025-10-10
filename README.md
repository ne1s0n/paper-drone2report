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

`python drone2report/drone2report.py paper-drone2report/case_studies/case-study-1/RGB_tobacco_leaves_GLI.ini`

3. Produce a thumbnail of the tobacco leaves image with threshold on GLI > 0.1. Use [drone2report](https://github.com/ne1s0n/drone2report) with the configuration file [RGB_tobacco_leaves_thumbnails.ini](case_studies/case-study-1/RGB_tobacco_leaves_thumbnails.ini) 

`python drone2report/drone2report.py paper-drone2report/case_studies/case-study-1/RGB_tobacco_leaves_thumbnails.ini`

#### Barley field

1. Distribution of GLI index values: the same thing we did for the tobacco leaves image, only now we are using shortcuts for the `--basefolder` and `--target_dir` command-line arguments.
   
`python scripts/get_index_values.py -b </path/to/my/project/folder> -s </path/to/results/folder> --fname data/barley_field/barley_field.tif --vix GLI`

2. Thresholding: we produce thumbnails for the barley field image at different GLI thresholds, and calculate the GLI index using only pixels above each threshold value. We use [drone2report](https://github.com/ne1s0n/drone2report) with the configuration file [RGB_barley_field_GLI_thumbnails.ini](case_studies/case-study-1/RGB_barley_field_GLI_thumbnails.ini) to produce thumbnails and calculate the index values. The thumbnails are produced in one run of the software; to calculate the index values at each threshold, we need to run [drone2report](https://github.com/ne1s0n/drone2report) as many times as there are thresholds (setting the `[TASK thumbnail]` to `False`, to avoid regenerating the thumbnail image files at each iteration): we can do this manually, each time changing the configuration file; or, we can generate the configuration files dynamically using a `python` or `bash` (or any other language) script and an iterative for loop. 

### Case study n. 2 - monitoring vegetation indices over time

For this case study we use image data from the same barley field as in case study n. 1: however, here we use multiple plots instead of one single plot.
It is typical, in plant experimental designs (especially in crops), to have one accession (variety, genotype) per plot.

When you have several images from multiple plots, to get vegetation indices using **drone2report** you can either: 
i) add several data sections in the configuration (.ini) file, one for each image, then run drone2report just once (example .ini file for two images: [RGB2_GLI_HUE.ini](case_studies/case-study-2/RGB2_GLI_HUE.ini); 
or ii) iterate over the number of images, automatically (or manually) generating each .ini file, thus running drone2report as many times as there are images.

A simple example using the provided .ini file for two input images might run as follows:

`python drone2report/drone2report.py paper-drone2report/case_studies/case-study-2/RGB2_GLI_HUE.ini`

Once you have run `drone2report` to process image data over several successive time points, you will end up with a file like [Fiorenzuola_RGB-GLI-HUE.xlsx](data/Fiorenzuola_RGB-GLI-HUE.xlsx): this is a spreadsheet with average GLI and HUE index values for 264 barley accessions from 10 successive flights over the growing season.

You can now parse this file with e.g. the R script [plot_time_curves.R](scripts/plot_time_curves.R) to obtain average index values for each accession at each flight and then plot these against time
