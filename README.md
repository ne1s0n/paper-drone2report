Repository for code and data used for the software article on [drone2report](https://github.com/ne1s0n/drone2report), to be submitted to [Plant Methods](https://plantmethods.biomedcentral.com/).
This work is partly supported by the research project [Polyploidbreeding](https://polyploidbreeding.ibba.cnr.it/).

### Data

- [TODO]: description of data
- [TODO]: prepare clean config.ini files to reproduce the different examples

### Case study n. 1

Calculate GLI index values for each pixel of the tobacco leaves RGB image:

`python scripts/get_index_values.py --base_folder </path/to/my/project/folder> --target_dir </path/to/results/folder> --fname data/tobacco_leaves/tobacco_leaves.tif --vix GLI`
