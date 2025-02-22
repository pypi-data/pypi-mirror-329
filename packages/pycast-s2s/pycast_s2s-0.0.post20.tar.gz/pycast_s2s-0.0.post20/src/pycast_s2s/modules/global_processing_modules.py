# Packages
import logging

import dask

import eccodes
import cfgrib

import xarray as xr

import pandas as pd


from pycast_s2s.modules import helper_modules

import xarray as xr

@dask.delayed
def gauss_to_regular(global_config, year, month, variable, mode):
    """
    Convert forecast data on Gaussian grids to regular grid using CDO.

    Parameters:
    - global_config (dict): A dictionary containing global configuration settings.
    - year (int): The year for which to perform the conversion.
    - month (int): The month for which to perform the conversion.
    - variable (str): The variable for which to perform the conversion.
    - mode (str): "1" represents a transformation per variable, "2" represents the transformation of the all-in-one file mode

    Returns:
    - dask.delayed: A delayed object representing the execution of the function.

    This function converts Gaussian gridded forecast data to a regular grid using
    the Climate Data Operators (CDO) tool. 

    Raises:
    - Exception: If an error occurs during the conversion process.

    Usage Example:
    ```python
    gauss_to_regular('in.grb', 'out.nc')
    ```

    Note: This function uses the `run_cmd` utility function to execute the CDO command.
    """

    if int(mode)==1:
        flenme_grb = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_{variable}_{year}{month:02d}.grb"
        flenme_nc = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_{variable}_{year}{month:02d}.nc"
    
    if int(mode)==2:
        flenme_grb = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_24h_{year}{month:02d}.grb"
        flenme_nc = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_24h_{year}{month:02d}.nc"
    print(flenme_grb)
    print(flenme_nc)
    cmd = (
        "cdo",
        "-O",
        "-f",
        "nc4c",
        "-z",
        "zip_6",
        "-P",
        "40",
        "setgridtype,regular",
        str(flenme_grb),
        str(flenme_nc),
    )
  
    try:
        helper_modules.run_cmd(cmd)
        logging.info(
            f"Gauss to regular: Remapping complete for {flenme_grb}"
        )
    except Exception as e:
        logging.error(
            f"Gauss to regular: Remapping failed for {flenme_grb}: %s",
            str(e),
            exc_info=True
        )

def preprocess_rename(ds, mapping_dict=None):
    """
        This routine is called when opening "unprocessed" NetCDF-Files that might still have some grib-codes 
        instead of actual variable names. It is still a untested demonstrator but, basically, should do the job...

    """
    # TODO: Get the variables from the mapping file 
    # For now, we simply use an example dict
    if mapping_dict is None:
        mapping_dict =  {
            "var228": "tp",
            "var55": "mean2t24",
            "var52": "mn2t24",
            "var51": "mx2t24",
            "var169": "ssrd"
        }

    mapping_vars = list(mapping_dict.keys())

    # Get the data# Get list of data variables
    data_vars = list(ds.data_vars) 

    renamed = False
    for mapping_variable, data_variable in itertools.product(mapping_vars, data_vars):
        if mapping_variable == data_variable and mapping_dict[data_variable] != data_variable:
            # We have found a match and the new name is different
            ds = ds.rename({data_variable: mapping_dict[data_variable]})
            renamed = True
            
    if renamed is False:
        logging.info('Nothing to rename - no matching variable names found')


            
    return ds


#def restructure_files(flenme_nc, separate_vars=True, separate_ens=False):
#    # Get the filename of the current NetCDF-file (for which gauss-to-regular has been executed)
#    ds = xr.open_mfdataset(flenme_nc, preprocess=preprocess_rename)
#    
#    # Get list of data variables
#    data_vars = list(ds.data_vars) 
#    
#    nr_ens = 51
#    
#    if separate_vars == True:
#        if separate_ens == False:
#            for var in data_vars:
#                for ens in range(nr_ens):
                    
                    
    
    
    
def rename_variable(global_config, year, month, variable):
    """
        Rename specific variables in a NetCDF dataset and save the modified dataset. This function takes a NetCDF dataset identified by the provided global configuration,
        year, and month, and renames specific variables within the dataset. The renamed variables
        are defined within the function. After renaming, the modified dataset is saved back to
        the original NetCDF file.
        
        Renamed variables:
         - 'var228' to 'tp'
         - 'var55' to 'mean2t24'
         - 'var52' to 'mn2t24'
         - 'var51' to 'mx2t24'
         - 'var169' to 'ssrd'

         Parameters:
            - global_config (dict): Global configuration settings, including 'raw_directory' and 'raw_forecasts' prefix.
            - year (int): Year of the dataset.
            - month (int): Month of the dataset.
            - variable (str): Variable name to be processed in the dataset.

        Returns:
            None
    """
          
    flenme_nc = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_{variable}_{year}{month:02d}.nc"
    
    # open current dataset
    ds = xr.open_dataset(flenme_nc)
    
    # rename variable here
    if 'var228' in ds.data_vars:
        ds = ds.rename({'var228': 'tp'})

    if 'var55' in ds.data_vars:
        ds = ds.rename({'var55': 'mean2t24'})

    if 'var52' in ds.data_vars:
        ds = ds.rename({'var52': 'mn2t24'})
    
    if 'var51' in ds.data_vars:
        ds = ds.rename({'var51': 'mx2t24'})

    if 'var169' in ds.data_vars:
        ds = ds.rename({'var169': 'ssrd'})
    
    #ToDo: add the strd here
    ds.to_netcdf(
            flenme_nc,
            'w',
            # "NETCDF4_CLASSIC",
            {"{variable}": {"zlib": True}}
            )


def transform_precip(ds):
    
    for var in ds.data_vars: 
        
        # Do some unit-conversion
        if var == 'tp':
            ds['tp'] = ds['tp'] * 1000
            
        # Calculate differences for accumulated variables
        if var == 'tp' or var == 'ssrd':
            ds = ds.diff(dim='step')
            
    return ds

#@dask.delayed
def unpack_forecasts(attribute_config, variable_config, filename_in, filename_out):
    
    # Get coordinates from actual forecast
    coords = helper_modules.get_coords_from_frcst(filename_in, 'grib')
    
    # Open the current forecast
    dta = xr.open_mfdataset(filename_in, engine='cfgrib', backend_kwargs={"indexpath": ''}, parallel=True, chunks='auto', preprocess=transform_precip).load()
    # Get the coordinates of the forecast
    
    
    # Rename the coordinate variables
    dta = dta.rename({'number': 'ens', 'latitude': 'lat', 'longitude': 'lon'})
    
    # Get the time-values
    time = dta.valid_time.values
    
    # Calculate "new" valid time
    time = time - pd.Timedelta('1D')
    
    # Replace the step-variable so that we can simply use the update_global_attribute_function
    coords['time'] = time
    
    attribute_config = helper_modules.update_global_attributes(attribute_config, None, coords, 'Global')
    
    # Assign the new time values to the step-variable
    dta = dta.assign_coords(step=time)
    
    # Delete time, valid-time and surface coordinate variables
    dta = dta.drop_vars(['time', 'valid_time', 'surface'])
    
    # Rename the step variable to time
    dta = dta.rename({'step': 'time'})
    
    # Set global attributes
    dta.attrs = attribute_config
    
    # Get the encoding-dict for setting compression, scaling_factor and add_offset.
    encoding = helper_modules.set_encoding(variable_config, coords)
    
    # We need to switch the order of the time- and ens-dimension to be more CF-consistent...
    dta = dta.transpose("time", "ens", "lat", "lon").compute()
    
    for var in dta.data_vars:
        
                        
        # This is horribly nasty and we should move it to another place...
        if var == 'mean2t24':
            dta = dta.rename({'mean2t24': 't2m'})
            var_out = 't2m'
        elif var == 'mn2t24':
            dta = dta.rename({'mn2t24': 't2min'})
            var_out = 't2min'
        elif var == 'mx2t24':
            dta = dta.rename({'mx2t24': 't2max'})
            var_out = 't2max'
        elif var == 'tp':
            var_out = 'tp'
        elif var == 'ssrd':
            var_out = 'ssrd'
        elif var == 'strd':
            var_out = 'strd'
            
        # Set the variable attributes
        dta[var_out].attrs = {
            "standard_name": variable_config[var_out]["standard_name"], 
            "long_name": variable_config[var_out]["long_name"],
            "units": variable_config[var_out]["units"],
        }
        
        # Explicitely rewmove the coordinates-attribute as this is causing some warnings when used, e.g,, with CDO
        dta[var_out].encoding["coordinates"] = None
         
        # Write the output to NetCDF.   
        dta.to_netcdf(
            filename_out,
            mode="w",
            engine="netcdf4",
            encoding={
			    var_out: encoding[var_out], 
			    'ens': encoding['ens'],
			    'time': encoding['time'],
			    'lat': encoding['lat'],
			    'lon': encoding['lon']
		    },
        )
    

    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
