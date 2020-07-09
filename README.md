# Introduction
This repository contains scripts developed to download and retrieve National Water Model reanalysis data for specified locations. 

1. First, follow instruction in [here](https://github.com/igarousi/XSEDE/tree/master/run_notebooks_on_comet) to run a jupyterlab/jupyter notebook on COMET. After openning jupyter lab, browse to the code directory and do the following.

2. **NWM_RRv2_Download.ipynb**: This jupyter notebook downloads the National Water Model (NWM) retrospective reanalysis data. Two batch scripts are used within this notebook.

3. **run.slurm.annual.large.short**: Submit this slurm schedular (on a terminal) that runs **NWM_RRv2_Retrieve.py** script on a compute node (large memory). This is a time consuming process. That is why it needs to be run for each year separately. Make sure to define `year` in the slurm batch script. It usually takes ~ 12 hours for one year to be completed. Results will be saved as zipped CSV files in output directory.  

4. **NWM_RRv2_Pre-processing.ipynb**: This jupyter notebook uses results from NWM_RRv2_Retrieve.py (i.e., zipped CSV files) to create single CSV for specified variables. 


# Directory Description

* **code**: Includes batch scripts, python scripts, and IPython jupyter notebooks used to install gsutil tool, use gsutil to download NWM reanalysis data, and retrieve required variables for specific locations (i.e., SNOTEL gages).

* **input**: Includes a CSV file that contains SNOTEL information (e.g. latitudes, longitudes, ...) and a text file that contains the name of varibales of interest (e.g. SNEQV which stands for snow water equivalent). *This directory should also include one example of NWM reanalysis LDASOUT output. The size of this file is large and not uploaded on GitHub. You can get one from [here](https://console.cloud.google.com/storage/browser/national-water-model-v2/full_physics/?pli=1).*


