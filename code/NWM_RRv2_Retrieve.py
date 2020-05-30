# This python script uses downloaded netcdf files to retrieve different 
# variables (defined in variable input) that are inputs to or outputs
# from the Noah-MP land surface model, such as snow water equivalent,
# albedo, snow covered fraction, ... 
# The script retrieves variables at specified locations (snotel gages).
# Due to the large size of NWM netcdf files, I will use this script
# for each year separately. Results will be zipped csv files that include
# retrieved values of selected variables at all snotel gages 
# for a specified year. **[Saving as zip files resolve memory issues]**
# The code is called within slrum job schedular. 


# Import libraries
import urllib.request 
import pandas as pd 
import os
import sys
import argparse
import numpy as np
import glob as gb
import netCDF4
import xarray as xr
import pyproj
from datetime import datetime

def Get_NWM_values(year, month, data_dir, variable, Site_Info, output_dir, output_name_2):

    '''
    This function takes start and end dates as well as the result Get_NWM_indices 
    function as inputs. It loops over all available downloaded NWM files and retrieves 
    the magnitudes of the variable of interest.
    
    year:
    data_dir:           The path to the reanalysis data
    variable:           The name of the varibale of interest
    Site_Info:          A CSV file includig indices information of gages. Results of Get_NWM_indices function.
    output_path:        The path to save results
    output_name:        The name of the csv file containing results of this function.
    '''  
    
    # Use open_mfdataset from xarray to open netcdf files and combine them based on time
    # Dask divides arrays into small pieces, called chunks, each of which is presumed to
    # be small enough to fit into memory. 
    # drop_variables=['ACCET', 'COSZ', 'SOIL_M', 'SOIL_W', 'UGCRNOFF', 'SFCRNOFF', 'HFX', 'LH']
    data = xr.open_mfdataset(os.path.join(data_dir, f'{year}/{year}{month}*'), 
                                          combine='nested', 
                                          concat_dim='Time',  
                                          chunks={'y':1000 , 'x':1000})
    
    print('open_mfdataset is finished.')
    
    xarr = xr.DataArray(Site_Info['Xindex'], dims="Station_ID", coords={"Station_ID": Site_Info['Station_ID']})
    yarr = xr.DataArray(Site_Info['Yindex'], dims="Station_ID", coords={"Station_ID": Site_Info['Station_ID']})
    select = getattr(data.isel(x=xarr, y=yarr), variable).to_series().reset_index().dropna().reset_index()
    
    print('isel is finished.')
    print(output_name_2)
    
    # Rename/add columns
    select.rename(columns={variable: f'{variable}_{getattr(data, variable).units}'}, inplace=True)
    
    # Save dataframe, using a loop due to error related to disk quota exceedance when saving a large file
    select.to_csv(os.path.join(output_dir, f'{output_name_2}.zip'),
              encoding='utf8',
              compression=dict(method='zip', archive_name=f'{output_name_2}.csv'),
              quoting=1,
              sep=',',
              index=False)
 
    return select


def main(input_dir, output_dir, data_dir, dataset, nrcs_file, year, month, variable, output_name_1, output_name_2):
   
    # Data Acquisition
    Site_Info = pd.read_csv(os.path.join(output_dir, output_name_1))
    start_time=datetime.now()
    print('Started at: ', start_time)
    NWM_values = Get_NWM_values(year, month, data_dir, variable, Site_Info, output_dir, output_name_2)
    print(datetime.now() - start_time)


if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    data_dir = sys.argv[3]
    dataset = sys.argv[4]
    nrcs_file = sys.argv[5]
    year = sys.argv[6]
    month = sys.argv[7]
    variable = sys.argv[8]
    output_name_1 = sys.argv[9]
    output_name_2 = sys.argv[10]

    main(input_dir, output_dir, data_dir, dataset, nrcs_file, year, month, variable, output_name_1, output_name_2)

