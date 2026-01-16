Repository for code and data used for the software article on [drone2report](https://github.com/ne1s0n/drone2report), 
currently under submission.
This work is partly supported by the research project [Polyploidbreeding](https://polyploidbreeding.ibba.cnr.it/) (PRIN 2022).

## Table of Contents

 1. [Data description](#Data-description)
 2. [Case study n. 1: thresholding](#case-study-n-1---thresholding)
 3. [Case study n. 2: monitoring vegetation indices over time](#case-study-n-2---monitoring-vegetation-indices-over-time)
 4. [Case study n. 3: detecting lodging from DEM files](#case-study-n-3---detecting-lodging-from-DEM-files)
 5. [Case study n. 4: loading multisource data, optimize an index](#case-study-n-4---loading-multisource-data-and-optimizing-an-index)
 6. [Case study n. 5: deep learning for image classification](#case-study-n-5---deep-learning-for-image-classification)

### Data description

As input for the case studies illustrated in this article, we used image data on: 

- i) barley field plots from the project [Polyploidbreeding](https://polyploidbreeding.ibba.cnr.it/)
- ii) tobacco leaves from [GRABSEEDS](https://github.com/tanghaibao/jcvi/wiki/GRABSEEDS) ([Tang et al. 2024](https://plantmethods.biomedcentral.com/articles/10.1186/s13007-024-01268-2))
- iii) soybean weed detection from [KAGGLE](https://www.kaggle.com/datasets/fpeccia/weed-detection-in-soybean-crops) repository

You will find the data for the case studies mainly in the [data/](data/) folder, or in the [results/](results/) folder in case of intermediate data/results; 
however, the precise location of input data is detailed in the description of each case study that you find below. In case of
large dataset a [figshare](https://doi.org/10.6084/m9.figshare.30327727) has
also been prepared.

---

### Case study n. 1 - thresholding

#### Tobacco leaves

1. Calculate GLI index values for each pixel of the tobacco leaves RGB image. We use the following `python` script specifying the project folder (`--base_folder`), the target folder for results (`--target_dir`), the name of the image file to be processed (`fname`), the vegetation index that we want to calculate (`--vix`), and the channels in the image (`--chan`): 


`python scripts/get_index_values.py --base_folder </path/to/my/project/folder> --target_dir </path/to/results/folder> --fname data/tobacco_leaves/tobacco_leaves.tif --vix GLI --chan 'red,green,blue'`

2. Apply threshold to remove background noise and calculate the GLI index only on tobacco leaves. You will use `drone2report` (from https://github.com/ne1s0n/drone2report) with the configuration file [RGB_tobacco_leaves_GLI.ini](case_studies/case-study-1_thresholding_GLI/RGB_tobacco_leaves_GLI.ini) 

`python drone2report/drone2report.py paper-drone2report/case_studies/case-study-1/RGB_tobacco_leaves_GLI.ini`

3. Produce a thumbnail of the tobacco leaves image with threshold on GLI > 0.1. Use [drone2report](https://github.com/ne1s0n/drone2report) with the configuration file [RGB_tobacco_leaves_thumbnails.ini](case_studies/case-study-1_thresholding_GLI/RGB_tobacco_leaves_thumbnails.ini) 

`python drone2report/drone2report.py paper-drone2report/case_studies/case-study-1/RGB_tobacco_leaves_thumbnails.ini`

#### Barley field

1. Distribution of GLI index values: the same thing we did for the tobacco leaves image, only now we are using shortcuts for the `--basefolder` and `--target_dir` command-line arguments.
   
`python scripts/get_index_values.py -b </path/to/my/project/folder> -s </path/to/results/folder> --fname data/barley_field/barley_field.tif --vix GLI`

2. Thresholding: we produce thumbnails for the barley field image at different GLI thresholds, and calculate the GLI index using only pixels above each threshold value. We use [drone2report](https://github.com/ne1s0n/drone2report) with the configuration file [RGB_barley_field_GLI_thumbnails.ini](case_studies/case-study-1_thresholding_GLI/RGB_barley_field_GLI_thumbnails.ini) to produce thumbnails and calculate the index values. The thumbnails are produced in one run of the software; to calculate the index values at each threshold, we need to run [drone2report](https://github.com/ne1s0n/drone2report) as many times as there are thresholds (setting the `[TASK thumbnail]` to `False`, to avoid regenerating the thumbnail image files at each iteration): we can do this manually, each time changing the configuration file; or, we can generate the configuration files dynamically using a `python` or `bash` (or any other language) script and an iterative for loop. 

---

### Case study n. 2 - monitoring vegetation indices over time

For this case study we use image data from the same barley field as in case study n. 1: however, here we use multiple plots instead of one single plot.
It is typical, in plant experimental designs (especially in crops), to have one accession (variety, genotype) per plot.

When you have several images from multiple plots, to get vegetation indices using **drone2report** you can either: 
i) add several data sections in the configuration (.ini) file, one for each image, then run drone2report just once (example .ini file for two images: [RGB2_GLI_HUE.ini](case_studies/case-study-2_HUE_over_time/RGB2_GLI_HUE.ini); 
or ii) iterate over the number of images, automatically (or manually) generating each .ini file, thus running drone2report as many times as there are images.

A simple example using the provided .ini file for two input images might run as follows:

`python drone2report/drone2report.py paper-drone2report/case_studies/case-study-2/RGB2_GLI_HUE.ini`

Once you have run `drone2report` to process image data over several successive time points, you will end up with a file like [Fiorenzuola_RGB-GLI-HUE.xlsx](data/Fiorenzuola_RGB-GLI-HUE.xlsx): this is a spreadsheet with average GLI and HUE index values for 264 barley accessions from 10 successive flights over the growing season.

You can now parse this file with e.g. the R script [plot_time_curves.R](scripts/plot_time_curves.R) to obtain average index values for each accession at each flight and then plot these against time; this is a script with customisable parameters in the heading section:

```r
#config
infile = 'paper-drone2report/data/Fiorenzuola_RGB-GLI-HUE.xlsx'
target_index = c('GLI_mean', 'HUE_mean')
outfile = 'paper-drone2report/results/time_curves.png'
number_of_plotted_lines = 20                                     ## n. of lines to draw
highlight_these_lines = c(157, 36)                               ## IDs of lines to highlight
```

After setting the parameters, you can run the R script from the command line as:

`Rscript scripts/plot_time_curves.R`

---

### Case study n. 3 - detecting lodging from DEM files

For this case study, we use the DEM file (digital elevation model) from the same barley field used in case studies n. 1 and n. 2.
The DEM file is quite large (~500 MB), therefore it is not included in this `Github` repository, but has been uploaded 
to [figshare](https://doi.org/10.6084/m9.figshare.30327727) (`case-study-3/`), together with the corresponding shape file.

The configuration file [DEM_barley_field_height.ini](case_studies/case-study-3_DEM_height/DEM_barley_field_height.ini) will instruct **drone2report** 
to extract the average height for each plot from the DEM file (as sepcified in the shape file: there are 264 plots in the barley field, one per barley accession).

However, to detect lodging (i.e. the reduction of height over time) we need to process the DEM files from multiple successive flights.
As we saw in [case study n. 2](#case-study-n-2---monitoring-vegetation-indices-over-time), when you need to process multiple image files you can
either write one single configuration file with many `[DATA]` sections, or generate multiple configuration files, one per file.

Let's assume that you have done it: the end results will be a .csv file with the average height for each plot (barley accession) and each flight (each DEM file)
([indexes_F_Dem.csv](data/indexes_F_Dem.csv)).
The first step is to normalise the plant height relative to the baseline, i.e. the height measured in the DEM file of the first flight.
We will use the [baseline_height.R](scripts/baseline_height.R) script, after modifying appropriately the configuration parameters (beginning of the script):
you will need to specify your paths to the .csv file with the average height per plot and flight.

```r
# config
  config = rbind(config, data.frame(
    prjfolder = "paper-drone2report",
    input_file = "data/barley_field/case-study-3/indexes_F_Dem.csv",
    outdir = "results",
    pattern = "_dem", ## suffix of dataset name that follows the date
    force_overwrite = FALSE
  ))
```

```r
Rscript scripts/baseline_height.R
```

This will produce the file [normalised_height.csv](results/normalised_height.csv) with normalised heights (per flight, per accession), 
ready to be plotted (Figure 6, B in the paper) using the [plot_index.R](scripts/plot_index.R) script, after modifying appropriately the configuration parameters (beginning of the script):

```r
# config
  config = rbind(config, data.frame(
    prjfolder = "paper-drone2repor",
    analysis_folder = "veg_indexes",
    input_file = "results/normalised_height.csv",
    label = "average height (m)",
    outdir = "results",
    pattern = "_dem", ## suffix of dataset name that follows the date
    index_column = "height_mean", ## name of index to plot (column in the csv file)
    force_overwrite = FALSE
  ))
```

```r
Rscript scripts/plot_index.R
```

---

### Case study n. 4 - loading multisource data and optimizing an index

For this case study, three type of data were available: RGB, multispecral,
and thermal. The drone flown over the Fiorenzuola field on June 12, 2024
(referred with the code 240612).

Given that these are real orthomosaic photos and not small subsets like in
the other case studies, the data has been uploaded on [figshare](https://doi.org/10.6084/m9.figshare.30327727).
As a first step, download the data (three tif images, plus a subfolder with all
the shape files, which are used to define the ROIs). It's about 4.5 GB of data.

There is only one .ini file accompanying this case study, called
[multisource_optimize.ini](case_studies/case-study-4_multisource_optimize_index/multisource_optimize.ini).
In its default state it will do nothing (no data load, no task invocation).
You can start by activating (setting `active=True`) the `[DATA thermal]`
section. Out of the three images available, the thermal data is the smaller and thus faster to be loaded, ideal for tests.

In this way drone2report will just load the image. You can thus check if all paths are correct, and then proceed to the next, more computational-heavy steps.

**Indices baselines**: the first step would be to compute the GLI index for RGB images and NDVI index for multispectral images. This is the "standard" procedure and gives us a target for index optimization, later. To do so:

- activate the `[DATA RGB_240612]` section, turn off all other `[DATA]` sections
- activate the `[TASK indexes]`, uncommenting the line that asks for GLI. Keep in mind that if you ask for impossible indices (e.g. NDVI on an RGB image) the output file will contains empty/NA values
- collect the data under the proper outfolder
- [optional] you may want to compute the correlation between the computed GLI and the final trait (Heading Date). You find the data in the [Fiorenzuola_phenos.csv](case_studies/case-study-4_multisource_optimize_index/Fiorenzuola_phenos.csv) file. Match the plot using the `gid` column

The above steps should be repeated using the [DATA MULTISPECTRAL_240612] section with NDVI index. If all went well you should produce a correlation of 0.129 (RGB+GLI) and 0.102 (multispectral+NDVI). These values are the baseline, to be improven by the optimization process.

**Loading a multisource dataset** Operationally, this is a very simple step; just deactivate all `[DATA]` and `[TASK]` sections, and leave active only `[DATA MULTISOURCE]`. Before doing that, however:

- note the internal strucure of `[DATA MULTISOURCE]`. While with other `[DATA]` sections there's only one `orthomosaic` field and one `channels` field, here we have three plus three of them. It makes sense, one per orthophoto
- channel names must not create conflict. For example, there is a "red" channel both in the RGB image and in the multispectral one. This would create confusion, because if two different channels are called "red" there's no way to distinguish them. That's why in the `channels_multispectral` you will find "red_ms", "green_ms", "blue_ms"
- loading a multisource image require to load the (three) single images, then interpolate all the data (for different image resolution) and reproject everything to a common [SRS](https://en.wikipedia.org/wiki/Spatial_reference_system). It can take some time, depending on your machine

Once the loading is complete you can do computation on this newly created 14-channels image (3 channels for RGB, 10 channels for multispectral, 1 channel for thermal).

**Optimizing an index** Index optimization is a done using a custom task, which is defined in file [optimize_index.py](case_studies/case-study-4_multisource_optimize_index/optimize_index.py). By convention, the task is a python class named as the file that defines it. Follow these steps:

- copy the [optimize_index.py](case_studies/case-study-4_multisource_optimize_index/optimize_index.py) into your python installation of drone2report under folder `d2r/tasks`
- activate `[DATA MULTISOURCE]` section and turn off all other `[DATA]` sections. Alternativel, you could activate only the `[DATA RGB_240612]`, which will run much faster
- activate the `[TASK optimize_index]`, and de-activate all other `[TASK]`
- run drone2report. It should say that it starts with a random X0, and it will run for a while (possibly hours, depending on your machine)

Internally, the task is optimizing the following index:

```
		       linear_combination(channels) + constant
custom_index = -------------------------------------------------------
		       another_linear_combination(channels) + another_constant

```

So, if we had only three RGB channels, it would optimize:

```
		           w1*R + w2*G + w3*G + w4
custom_index_RGB = -----------------------
		           w5*R + w6*G + w7*G + w8

```

Optimizing in this context means to find the best combination of weights (w1, ..., w8 for RGB images) that gives the maximum correlation between the array of index values (averaged per plot) and the real measured trait (heading date, in this case).

The number of weights to be optimized is always `2*number_of_channels+2`

The system will run for a while,and you can monitor its progress via the logfile specified via the `outfolder` and `outfile` fields. This is a csv table that reports the progress of the optimization process. If you stop the optimization and then start again, the task will try to load the data from the last line of the logfile.

Depending on what `[DATA]` sections are active the tool will optimize either RGB, multispectral, or multisource data. Keep in mind that optimization is a stochastic process and starting again over and over will produce different trajectories.

---

### Case study n. 5 - deep learning for image classification

For this case study a trained deep learning model is applied to a set of existing tif drone images. The output of the classification is stored in a .csv file.

To reproduce the results:

1. go to the [figshare repository](https://doi.org/10.6084/m9.figshare.30327727) and download the folder `case-study-resnet-classification`. This contains the trained model (a keras save, `resnet50_final_notest.keras`) and a folder with the images to be classified (`weed-detection-in-soybean-crops`). Notice that there are four subfolders, one per class
2. from this github repo download the file `classify_resnet.py`, which contains a drone2report TASK definition. This file must be copied into your drone2report installation folder, and in particular in the `d2r/tasks` subfolder
3. from this github repo download the `classify_resnet.ini`, which contains the configuration useful for the assigned task. Before running drone2report you need to change this .ini file and make it point to the proper data folder (the place where you saved the data. In particular, change the `infolder=...` value to point to the correct folder

If all the setup is correct you will run drone2report, which will spit a generous log. The first `DATASET SETUP` section will contain 40 repetitions of something similar to the following:



>    
    DATASET grass_1
    Opening image file /home/nelson/paper-drone2report/case_studies/case-study-5_image_classification//weed-detection-in-soybean-crops/grass/1.tif
     - projection:  PROJCS["WGS 84 / Pseudo-Mercator",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Mercator_1SP"],PARAMETER["central_meridian",0],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["Easting",EAST],AXIS["Northing",NORTH],EXTENSION["PROJ4","+proj=merc +a=6378137 +b=6378137 +lat_ts=0 +lon_0=0 +x_0=0 +y_0=0 +k=1 +units=m +nadgrids=@null +wktext +no_defs"],AUTHORITY["EPSG","3857"]]
     - geotransform:  minX= 0.0  xRes= 1.0  yRot= 0.0  minY= 0.0  xRot= 0.0  yRes= 1.0
     - size (cols, rows, bands): 264,272,3
     - band names:  ['red', 'green', 'blue']
     - value used for nodata pixels: None
>   
     Visible bands (rendered as RGB): ['red', 'green', 'blue']
>    
    opening shape file /home/nelson/paper-drone2report/case_studies/case-study-5_image_classification//weed-detection-in-soybean-crops/grass/1.shp
    - found 1 ROIs with fields ['id', 'gid', 'name', 'geometry']
    - fields used to uniquely identify a shape: ['gid']

The above section will be repeated 40 times, since we are loading 40 images.
The software will then enter the task execution phase: the deep learning model is loaded and applied to all images, one at a time.

The results of the predictions are saved in the `results` subfolder.

Tips and tricks:

- to run this case study a number of python modules should be installed, most notably tensorflow. Depending on your machine, this could range from very simple to very challenging. The dataset for this case study is small, so there's no need for actual GPU optimization, but your mileage may vary
- you may have a .tif image which is not a proper geotiff. This means that you have the image and nothing else: no shapefile, no projection information, nothing. Just the raster data. This case study includes a simple python utility called `build_shapefile.py` which creates stub, default values for all the missing files. It was used on this very dataset, too
- writing very long .ini files can be tedious and prone to errors. We included a small script to programmatically create the required file. Look into `classify_resnet.ini_builder.py` for inspirations for your future work














