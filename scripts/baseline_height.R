# script that normalises plant height as obtained from the DEM file
# relative to the baseline height (first flight in the series)
library("tidyverse")
library("data.table")


## PARAMETERS
args = commandArgs(trailingOnly=TRUE)
if (length(args) >= 1) {
  
  #loading the parameters
  if (file_ext(args[1]) %in% c("r","R")) {
    
    source(args[1])
    # source("Analysis/hrr/config.R")
  } else {
    
    load(args[1])
  }
  
} else {
  #this is the default configuration, used for development and debug
  writeLines('Using default config')
  
  #this dataframe should be always present in config files, and declared
  #as follows
  config = NULL
  config = rbind(config, data.frame(
    prjfolder = "paper-drone2report",
    input_file = "data/barley_field/case-study-3/indexes_F_Dem.csv", ## from drone2report
    outdir = "results",
    pattern = "_dem",
    force_overwrite = FALSE
  ))
}

## -- 
HOME <- Sys.getenv("HOME")
prjfolder = file.path(HOME, config$prjfolder)
outdir = file.path(prjfolder, config$outdir)

## read data file
fname = file.path(prjfolder, config$input_file)
dem = fread(fname)

writeLines(" - get date of first flight (baseline)")
dem$date = gsub(config$pattern,"",dem$dataset)
dem$date = as.Date(dem$date, "%y%m%d")

dates = sort(unique(dem$date))
print(paste("Selecting", dates[1], "as baseline for plant height"))

## get baseline data
dem_baseline <- dem |>
  filter(date == dates[1])

writeLines(" - normalise height by subtracting baseline")
dem$baseline_height = dem_baseline$height_mean[match(dem$gid, dem_baseline$gid)]
dem <- dem |>
  mutate(height_mean = height_mean - baseline_height)

writeLines(" - writing out normalised height file")
dem <- dem |> select(-c(baseline_height))

fname = file.path(outdir, "normalised_height.csv")
fwrite(x = dem, file = fname)
