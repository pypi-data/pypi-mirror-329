"""
This module provides functions for processing regional climate data, including:

- Preprocessing functions for forecasts and reference data (e.g., renaming coordinates, handling time dimensions).
- Truncating and remapping functions for both forecasts and reference data to a specified domain and grid.
- Calibration functions for forecasts, involving concatenation and rechunking of data.
- Utility functions for creating grid files and setting encoding parameters for NetCDF files.

The module utilizes libraries like Xarray, Dask, and CDO for data manipulation, parallel processing, and remapping operations.
"""

# Packages
import logging
import os
from os.path import exists

import zarr
import dask
import numpy as np
import pandas as pd

import xarray as xr
from scipy.interpolate import griddata
from rechunker import rechunk

# import dir_fnme
from pycast_s2s.modules.helper_modules import run_cmd, set_encoding

# Open Points
# 1. Paths are local, change them (pd/data)
# 2. Get information out of the parameter-file (which has to be changed, according to
#       Christof's draft)
# 3. Global attributes for nc-Files --> check, how the historic raw seas5-files for other
#       domains have been built and rebuilt for new domains
#  --> Change overall settings for nc-Files (global attributes, vars, etc.) within the module.py,
#       so that it can be used for all cases within the BCSD


# SEAS5 #
# Steps:
# 1. Load global SEAS5-Dataset
# 2. Cut out domain of interest
# 3. Remap to local grid
# 4. Store as high resolution dataset for the specific domain

global bbox


def create_grd_file(domain_config: dict, grid_file: str) -> str:
    """Creates a grid description file that is used for remapping the forecasts to the final resolution."""
    min_lon = domain_config["bbox"][0]
    max_lon = domain_config["bbox"][1]
    min_lat = domain_config["bbox"][2]
    max_lat = domain_config["bbox"][3]

    # Create regional mask with desired resolution
    grd_res = domain_config["target_resolution"]
    lat_range = int((max_lat - min_lat) / grd_res) + 1
    lon_range = int((max_lon - min_lon) / grd_res) + 1
    grd_size = lat_range * lon_range

    # grd_flne = f"{dir_dict['grd_dir']}/{fnme_dict['grd_dir']}"

    # if file does not exist, create regional text file for domain with desired resolution
    # --> Can be implemented and outsourced as function !!!!!
    content = [
        f"# regional grid\n",
        f"# domain: {domain_config['prefix']}\n",
        f"# grid resolution: {str(grd_res)}\n",
        f"gridtype = lonlat\n",
        f"gridsize = {str(grd_size)}\n",
        f"xsize = {str(lon_range)}\n",
        f"ysize = {str(lat_range)}\n",
        f"xname = lon\n",
        f"xlongname = Longitude\n",
        f"xunits = degrees_east\n",
        f"yname = lat\n",
        f"ylongname = Latitude\n",
        f"yunits = degrees_north\n",
        f"xfirst = {str(min_lon)}\n",
        f"xinc = {str(grd_res)}\n",
        f"yfirst = {str(min_lat)}\n",
        f"yinc = {str(grd_res)}\n",
    ]

    if not os.path.isfile(grid_file):
        with open(grid_file, mode="w") as f:
            f.writelines(content)
    else:
        print("File for regional grid already exists")

    return grid_file

def create_grid_ds(grid_file_path):
    """
    Reads a grid definition file and creates an xarray.Dataset for regridding with xESMF.

    Parameters:
        grid_file_path (str): Path to the grid definition file.

    Returns:
        xr.Dataset: An xarray dataset containing the latitude and longitude grid.
    """
    def read_grid_definition(file_path):
        """Reads a grid definition file and extracts grid parameters."""
        grid_params = {}

        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue  # Skip comments and empty lines
                key, value = line.split("=", 1)
                grid_params[key.strip()] = value.strip()

        return grid_params

    # Read grid paramet
    grid_params = read_grid_definition(grid_file_path)

    # Extract parameters
    xsize = int(grid_params["xsize"])
    ysize = int(grid_params["ysize"])
    xfirst = float(grid_params["xfirst"])
    yfirst = float(grid_params["yfirst"])
    xinc = float(grid_params["xinc"])
    yinc = float(grid_params["yinc"])

    # Generate coordinate arrays
    lon_values = np.linspace(xfirst, xfirst + (xsize - 1) * xinc, xsize)
    lat_values = np.linspace(yfirst, yfirst + (ysize - 1) * yinc, ysize)

    # Create new grid dataset
    grid_out = xr.Dataset(
        {
            "lat": (["lat"], lat_values),
            "lon": (["lon"], lon_values),
        }
    )

    return grid_out

### SEAS5 ###

def preprocess(ds):
    """Preprocesses an xarray Dataset by renaming and sorting coordinates.

    This function standardizes the longitude and latitude coordinates of a dataset,
    ensuring correct naming and ascending order. It also converts longitudes from
    the [0, 360] range to [-180, 180] if necessary.

    Args:
        ds (xr.Dataset): The input xarray Dataset.

    Returns:
        xr.Dataset: The preprocessed xarray Dataset.
    """
    # Rename longitude and latitude if necessary
    if "longitude" in ds.variables and "lon" not in ds.variables:
        ds = ds.rename({"longitude": "lon"})

    if "latitude" in ds.variables and "lat" not in ds.variables:
        ds = ds.rename({"latitude": "lat"})
        
    # Ensure latitudes are in ascending order
    if ds.lat[0] > ds.lat[-1]:  
        ds = ds.sortby(ds.lat)
        
    # Convert longitude format from [0, 360] to [-180, 180] if necessary
    if ds.lon.max() > 180:  
        ds.coords["lon"] = (ds.coords["lon"] + 180) % 360 - 180
        ds = ds.sortby(ds.lon)  #
            
    #ds.coords["lon"] = (ds.coords["lon"] + 180) % 360 - 180

    ds["lon"].attrs = {"standard_name": "longitude", "units": "degrees_east"}
    ds["lat"].attrs = {"standard_name": "latitude", "units": "degrees_north"}

    return ds


@dask.delayed
def truncate_forecasts(
    domain_config: dict,
    variable_config: dict,
    reg_dir_dict: dict,
    year: int,
    month: int,
    variable: str,
    file_in_override: list = None,  # Allow list for multiple ensemble members
    file_out_override: str = None   # Allow single string for output file
) -> None:
    """Truncates and saves forecast data for a specific region, year, and month.

    This function reads forecast data, selects a specified bounding box, and saves the
    truncated data to a NetCDF file. It handles both single ensemble member files and
    multiple ensemble member files.

    Args:
        domain_config (dict): Configuration dictionary for the domain.
        variable_config (dict): Configuration dictionary for the variable.
        reg_dir_dict (dict): Dictionary containing regional directory paths.
        year (int): The year of the forecast data.
        month (int): The month of the forecast data.
        variable (str): The name of the variable to process.
        file_in_override (list, optional): List of input filenames to override the default. Defaults to None.
        file_out_override (str, optional): Output filename to override the default. Defaults to None.

    Returns:
        None
    """

    bbox = domain_config["bbox"]

    # Add one degree in each direction to avoid NaNs at the boarder after remapping.
    #min_lon = bbox[0] 
    #max_lon = bbox[1]
    #min_lat = bbox[2]
    #max_lat = bbox[3] 

    if file_in_override is not None:
        file_in = file_in_override  # Use user-provided filenames
    else:
        file_template = domain_config['variable_mapping'][variable]['reforecasts']['filename']
        varname_forecasts = domain_config['variable_mapping'][variable]['reforecasts']['varname']

        if '{ens}' in file_template:
            file_in = file_template.format(year=str(year), month=f"{month:02d}", ens="*")
        else:
            file_in = file_template.format(year=str(year), month=f"{month:02d}")

    if file_out_override is not None:
        file_out = file_out_override
    else:
        file_out_default = f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{year}{month:02d}.nc"
        file_out = f"{reg_dir_dict['raw_forecasts_initial_resolution_dir']}/{file_out_default}"

    # Open dataset
    if isinstance(file_in, list):
        ds = xr.open_mfdataset(
            file_in,
            concat_dim="ens",
            combine="nested",
            parallel=True,
            chunks="auto",
            preprocess=preprocess,
        )
    else:
        ds = xr.open_mfdataset(
            file_in,
            parallel=True,
            chunks="auto",
            preprocess=preprocess,
        )
    
    # Here, we throw away all variables except for the variable that is currently processed.
    # This, however, is a bit nasty as in cases where multiple variables are in one file, we would
    # have to re-open the file when the next variable is processed...
    if file_in_override is not None:
        varname_forecasts = variable
        
    ds =  ds[varname_forecasts]
    
    resolution = ds.lat.values[1] - ds.lat.values[0]    
    
    # Get the resolution of the dataset so that we can add one more pixel in each direction
    min_lon = bbox[0] - 2*resolution
    max_lon = bbox[1] + 2*resolution
    min_lat = bbox[2] - 2*resolution
    max_lat = bbox[3] + 2*resolution
    
    # Select the coordinates that lie within the bounding box
    ds = ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon)) 
    
    # Create a simple coords-dictionary that holds all coordinates. 
    coords = {
        "time": ds["time"].values,
        "lat": ds["lat"].values.astype(np.float32),
        "lon": ds["lon"].values.astype(np.float32),
        "ens": ds["ens"].values,
    }

    # Transpose to CF-compliant ordering
    ds = ds.transpose("time", "ens", "lat", "lon") if "ens" in ds.dims else ds.transpose("time", "lat", "lon")

    # Retrieve the encoding dict that holds the information about how variables are written to the output NetCDFs
    encoding = set_encoding(variable_config, coords)

    # As there might be some pre-defined encoding parameter in the dataset, we first have to delete these. 
    ds.encoding = []

    # After that, we can write the output-NetCDF by using the new encoding parameter 
    try:
        ds.to_netcdf(file_out, encoding={varname_forecasts: encoding[variable], 'lat': encoding['lat'], 'lon': encoding['lon'], 'time': encoding['time']}, engine="netcdf4")
        logging.info(f"Truncate forecasts: succesful")
    except Exception as err:
        logging.error(f"Truncate forecasts: {err}")
        

@dask.delayed
def remap_forecasts(
    domain_config: dict,
    variable_config: dict,
    reg_dir_dict: dict,
    year: int,
    month: int,
    variable: str,
    grd_fle: str,
    file_in_override: list = None,  # Allow list for multiple ensemble members
    file_out_override: str = None   # Allow single string for output file
) -> None:
    """Remaps forecast data to a target grid and saves the result to a NetCDF file.

    This function reads forecast data, remaps it to a specified grid using interpolation,
    and saves the remapped data to a new NetCDF file. It handles both single ensemble
    member files and multiple ensemble member files.

    Args:
        domain_config (dict): Configuration dictionary for the domain.
        variable_config (dict): Configuration dictionary for the variable.
        reg_dir_dict (dict): Dictionary containing regional directory paths.
        year (int): The year of the forecast data.
        month (int): The month of the forecast data.
        variable (str): The name(s) of the variable(s) to process.
        grd_fle (str): Path to the grid file used for remapping.
        file_in_override (list, optional): List of input filenames to override the default. Defaults to None.
        file_out_override (str, optional): Output filename to override the default. Defaults to None.

    Returns:
        None
    """
    
    
    if file_in_override is not None:
        file_in = file_in_override  # Use user-provided filenames
    else:
        file_in_template = f"{domain_config['variable_mapping'][variable]['forecasts']['product_prefix']}_{variable}_{year}{month:02d}.nc"
        file_in = f"{reg_dir_dict['raw_forecasts_initial_resolution_dir']}{file_in_template}"

    if file_out_override is not None:
        file_out = file_out_override
    else:
        file_out_template = f"{domain_config['variable_mapping'][variable]['forecasts']['product_prefix']}_{variable}_{year}{month:02d}_{domain_config['target_resolution']}.nc"
        file_out = f"{reg_dir_dict['raw_forecasts_target_resolution_dir']}{file_out_template}"

    if file_in_override is not None:
        varname_forecasts = variable

    ds = xr.open_mfdataset(
            file_in,
            parallel=True,
            chunks="auto",
            preprocess=preprocess,
        )

    # Read the grid-description from the previously generated grid file
    grid_out = create_grid_ds(grd_fle)

    # Interpolate the forecasts to the target grid using a simple bilinear interpolation approach
    ds_interp = ds.interp(lat=grid_out.lat, lon=grid_out.lon)

    # Create a simple coords-dictionary that holds all coordinates. 
    coords = {
        "time": ds_interp["time"].values,
        "lat": ds_interp["lat"].values.astype(np.float32),
        "lon": ds_interp["lon"].values.astype(np.float32),
        "ens": ds_interp["ens"].values,
    }

    # Retrieve the encoding dict that holds the information about how variables are written to the output NetCDFs
    encoding = set_encoding(variable_config, coords)

    # As there might be some pre-defined encoding parameter in the dataset, we first have to delete these. 
    ds_interp.encoding = []

    # After that, we can write the output-NetCDF by using the new encoding parameter
    try:
        ds_interp.to_netcdf(file_out, encoding={varname_forecasts: encoding[variable], 'lat': encoding['lat'], 'lon': encoding['lon'], 'time': encoding['time']}, engine="netcdf4")
        logging.info("Remap forecasts: succesful")
    except Exception as err:
        logging.error(f"Remap forecasts: Something went wrong: {err}")
        
        

    
    
    #cmd = (
    #    "cdo",
    #    "-O",
    #    "-f",
    #    "nc4c",
    #    "-z",
    #    "zip_6",
    #    f"remapbil,{grd_fle}",
    #    str(file_in),
    #    str(file_out),
    #)

    #try:
    #    os.path.isfile(full_in)
    #    run_cmd(cmd)
    #except Exception as err:
    #    logging.error(f"Remap_forecast: file {full_in} not available")



def preprocess_reference(ds):
    """Preprocesses reference data by adjusting time coordinates and renaming variables.

    This function modifies the time dimension of a reference dataset to ensure
    consistent daily values throughout the year. It also standardizes longitude and
    latitude coordinates, converting longitudes to the [-180, 180] range if necessary.
    Additionally, it removes the "bnds" dimension if present.

    Args:
        ds (xr.Dataset): The input xarray Dataset.

    Returns:
        xr.Dataset: The preprocessed xarray Dataset.
    """
    
    # Create new and unique time values
    # set year
    year = ds.time.dt.year.values[0]
    # save attributes
    time_attr = ds.time.attrs

    # Create time values
    time_values = pd.date_range(f"{year}-01-01", f"{year}-12-31")

    # Set time values
    ds = ds.assign_coords({"time": time_values})
    ds.time.attrs = {
        "standard_name": time_attr["standard_name"],
        "long_name": time_attr["long_name"],
        "axis": time_attr["axis"],
    }

    # some other preprocessing
    if "longitude" in ds.variables:
        ds = ds.rename({"longitude": "lon"})

    if "latitude" in ds.variables:
        ds = ds.rename({"latitude": "lat"})

    ds = ds.sortby(ds.lat)
    ds.coords["lon"] = (ds.coords["lon"] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)

    ds["lon"].attrs = {"standard_name": "longitude", "units": "degrees_east"}
    ds["lat"].attrs = {"standard_name": "latitude", "units": "degrees_north"}

    # Drop var "time bounds" if necessary, otherwise cant be merged
    try:
        ds = ds.drop_dims("bnds")
    except:
        print("No bnds dimension available")

    return ds


@dask.delayed
def truncate_reference(
    domain_config: dict,
    variable_config: dict,
    reg_dir_dict: dict,
    year: int,
    variable: str,
) -> None:
    """Truncates and saves reference data for a specific region and year.

    This function reads reference data, selects a specified bounding box, and saves the
    truncated data to a NetCDF file. It handles different reference datasets, such as
    ERA5-Land, and applies specific preprocessing if necessary.
    
    Parameters
    ----------
    domain_config : dict 
        Configuration dictionary for the domain.
    variable_config : dict
        Configuration dictionary for the variable.
    reg_dir_dict : dict
        Dictionary containing regional directory paths.
    year : int
        The year of the reference data.
    variable : str
        The name of the variable to process.

    Returns
    -------
    None
    """
    bbox = domain_config["bbox"]

    # Add one degree in each direction to avoid NaNs at the boarder after remapping.
    min_lon = bbox[0] - 1
    max_lon = bbox[1] + 1
    min_lat = bbox[2] - 1
    max_lat = bbox[3] + 1

    file_in = domain_config['variable_mapping'][variable]['reference']['filename'].format(year=str(year))
    varname_reference = domain_config['variable_mapping'][variable]['reference']['varname']

    if domain_config['variable_mapping'][variable]['reference']['product_prefix'] == 'ERA5_Land':
        with dask.config.set(**{'array.slicing.split_large_chunks': True}):
            ds = xr.open_mfdataset(
                file_in,
                parallel=False,
                chunks={"time": 20},
                engine="netcdf4",
                preprocess=preprocess_reference,
                autoclose=True,
            )
    else:
        with dask.config.set(**{'array.slicing.split_large_chunks': True}):
            ds = xr.open_mfdataset(
                file_in,
                parallel=False,
                chunks={"time": 20},
                engine="netcdf4",
                autoclose=True,
            )
        
    file_out = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{year}.nc"
    full_out = f"{reg_dir_dict['reference_initial_resolution_dir']}/{file_out}"

    ds = ds.sel(lat=slice(min_lat, max_lat), lon=slice(min_lon, max_lon))
    
    coords = {
        "time": ds["time"].values,
        "lat": ds["lat"].values.astype(np.float32),
        "lon": ds["lon"].values.astype(np.float32),
    }

    encoding = set_encoding(variable_config, coords)

    try:
        ds.to_netcdf(full_out, encoding={varname_reference: encoding[variable], 'lat': encoding['lat'], 'lon': encoding['lon'], 'time': encoding['time']})
        logging.info(
            f"Truncate reference: succesful for variable {variable} and year {year}"
        )
    except:
        logging.info(
            f"Truncate reference: something went wrong for variable {variable} and year {year}"
        )

@dask.delayed
def remap_reference(
    domain_config: dict,
    variable_config: dict,
    reg_dir_dict: dict,
    year: int,
    variable: str,
    grd_fle: str,
    file_in_override: list = None,  # Allow list for multiple ensemble members
    file_out_override: str = None   # Allow single string for output file
) -> None:
    """Remaps reference data to a target grid and saves the result.

    This function reads reference data, interpolates it to a specified grid,
    and saves the remapped data to a NetCDF file. It handles various input and
    output file configurations.

    Parameters
    ----------
    domain_config : dict
        Configuration dictionary for the domain.
    variable_config : dict 
        Configuration dictionary for the variable.
    reg_dir_dict : dict 
        Dictionary containing regional directory paths.
    year : int 
        The year of the reference data.
    variable : str 
        The name of the variable to process.
    grd_fle : str 
        Path to the grid file used for remapping.
    file_in_override : list 
        (Optional) List of input filenames to override the default. Defaults to None.
    file_out_override : str 
        (Optional) Output filename to override the default. Defaults to None.

    Returns
    -------
        None
    """
    
    if file_in_override is not None:
        file_in = file_in_override  # Use user-provided filenames
    else:
        file_in_template = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{year}.nc"
        file_in = f"{reg_dir_dict['reference_initial_resolution_dir']}/{file_in_template}"

    if file_out_override is not None:
        file_out = file_out_override
    else:
        file_out_template = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{year}_{domain_config['target_resolution']}.nc"
        file_out = f"{reg_dir_dict['reference_target_resolution_dir']}/{file_out_template}"
        
    if file_in_override is not None:
        varname_reference = variable

    ds = xr.open_mfdataset(
            file_in,
            parallel=True,
            chunks="auto",
        )      
    
    
    grid_out = create_grid_ds(grd_fle)

    ds_interp = ds.interp(lat=grid_out.lat, lon=grid_out.lon)

    #lon_values, lat_values = np.meshgrid(grid_out.lon, grid_out.lat)
    #points = np.array([ds.lon.values.ravel(), ds.lat.values.ravel()]).T
    #values = ds[varname_forecasts].values.ravel()  #

    #regridder = xe.Regridder(ds, grid_out, "bilinear")

    # Apply regridding
    #ds_interp = regridder(ds)
    # Save the regridded data to a new file


    # Create a simple coords-dictionary that holds all coordinates. 
    coords = {
        "time": ds_interp["time"].values,
        "lat": ds_interp["lat"].values.astype(np.float32),
        "lon": ds_interp["lon"].values.astype(np.float32),
    }

    # Retrieve the encoding dict that holds the information about how variables are written to the output NetCDFs
    encoding = set_encoding(variable_config, coords)

    # As there might be some pre-defined encoding parameter in the dataset, we first have to delete these. 
    ds_interp.encoding = []

    # After that, we can write the output-NetCDF by using the new encoding parameter
    try:
        ds_interp.to_netcdf(file_out, encoding={varname_reference: encoding[variable], 'lat': encoding['lat'], 'lon': encoding['lon'], 'time': encoding['time']}, engine="netcdf4")
        logging.info("Remap forecasts: succesful")
    except Exception as err:
        logging.error(f"Remap forecasts: Something went wrong: {err}")
        
        

    #file_in = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{year}.nc"
    #full_in = f"{reg_dir_dict['reference_initial_resolution_dir']}/{file_in}"

    #file_out = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{year}_{domain_config['target_resolution']}.nc"
    #full_out = f"{reg_dir_dict['reference_target_resolution_dir']}/{file_out}"

    #cmd = (
    #    "cdo",
    #    "-O",
    #    "-f",
    #    "nc4c",
    #    "-z",
    #    "zip_6",
    #    f"remapbil,{grd_fle}",
    #    str(full_in),
    #    str(full_out),
    #)

    #try:
    #    os.path.isfile(full_in)
    #    run_cmd(cmd)
    #except Exception:
    #    logging.error(f"Remap_forecast: file {full_in} not available")

######### Old Crap #########

def rechunker_forecasts(
    domain_config: dict,
    variable_config: dict,
    dir_dict: dict,
    year: int,
    month: int,
    variable: str,
):

    fnme_dict = dir_fnme.set_filenames(
        domain_config,
        year,
        month,
        domain_config["raw_forecasts"]["merged_variables"],
        variable,
    )

    fle_string = f"{dir_dict['frcst_high_reg_dir']}/{fnme_dict['frcst_high_reg_dir']}"

    return fle_string


@dask.delayed
def rechunk_forecasts(
    domain_config: dict,
    variable_config: dict,
    dir_dict: dict,
    year: int,
    month: int,
    variable: str,
):

    month_str = str(month).zfill(2)

    # if domain_config['reference_history']['merged_variables'] == True:
    #    # Update Filenames
    #    fnme_dict = dir_fnme.set_filenames(domain_config, year, month_str,
    # domain_config['raw_forecasts']["merged_variables"])

    #    fle_string = f"{dir_dict['frcst_high_reg_dir']}/{fnme_dict['frcst_high_reg_dir']}"

    #    ds = xr.open_mfdataset(fle_string, parallel=True, engine='netcdf4', autoclose=True, chunks={'time': 50})

    #    coords = {'time': ds['time'].values, 'ens': ds['ens'].values, 'lat': ds['lat'].values.astype(np.float32),
    #              'lon': ds['lon'].values.astype(np.float32)}

    #    encoding = set_encoding(variable_config, coords, 'lines')

    #    final_file = f"{dir_dict['frcst_high_reg_lnch_dir']}/{fnme_dict['frcst_high_reg_lnch_dir']}"

    #    try:
    #        ds.to_netcdf(final_file, encoding=encoding)
    #        logging.info(f"Rechunking forecast for {month_str} successful")
    #    except:
    #        logging.error(f"Something went wrong during writing of forecast linechunks")
    # else:
    #    for variable in variable_config:
    # Update Filenames
    fnme_dict = dir_fnme.set_filenames(
        domain_config,
        year,
        month,
        domain_config["raw_forecasts"]["merged_variables"],
        variable,
    )

    fle_string = f"{dir_dict['frcst_high_reg_dir']}/{fnme_dict['frcst_high_reg_dir']}"

    ds = xr.open_mfdataset(
        fle_string,
        parallel=True,
        # chunks={"time": 'auto', 'ens': 'auto', 'lat': -1, 'lon': -1},
        chunks={"time": 50},
        engine="netcdf4",
        autoclose=True,
    )

    # ds = ds.chunk({"time": -1, 'ens': -1, 'lat': 1, 'lon': 1})

    coords = {
        "time": ds["time"].values,
        "ens": ds["ens"].values,
        "lat": ds["lat"].values.astype(np.float32),
        "lon": ds["lon"].values.astype(np.float32),
    }

    encoding = set_encoding(variable_config, coords, "lines")

    # Delete the chunksizes-attribute as we want to keep the chunks from above..
    # del encoding[variable]["chunksizes"]
    # del encoding[variable]["zlib"]
    # del encoding[variable]["complevel"]

    # compressor = zarr.Blosc(cname="zstd", clevel=3, shuffle=2)

    # encoding[variable]["compressor"] = compressor

    final_file = (
        f"{dir_dict['frcst_high_reg_lnch_dir']}/{fnme_dict['frcst_high_reg_lnch_dir']}"
    )

    try:
        ds.to_netcdf(final_file, encoding={variable: encoding[variable]})
        logging.info(
            f"rechunk_forecasts: Rechunking forecast for {year}-{month:02d} successful"
        )
    except:
        logging.info(f"rechunk_forecasts: Something went wrong for {year}-{month:02d}")

def calib_forecasts(domain_config, variable_config, dir_dict, syr, eyr, month_str):
    """Calibrates forecasts by concatenating and rechunking data.

    This function concatenates forecast data for a specified period (syr to eyr)
    and rechunks it for optimized storage and access. It handles both merged and
    individual variable files based on the 'merged_variables' configuration.

    Args:
        domain_config (dict): Domain configuration dictionary.
        variable_config (dict): Variable configuration dictionary.
        dir_dict (dict): Directory paths dictionary.
        syr (int): Start year for calibration.
        eyr (int): End year for calibration.
        month_str (str): Month string (e.g., "01").
    """
    file_list = []
    if domain_config["reference_history"]["merged_variables"]:
        for year in range(syr, eyr + 1):
            # Update Filenames
            fnme_dict = dir_fnme.set_filenames(
                domain_config,
                syr,
                eyr,
                year,
                month_str,
                domain_config["raw_forecasts"]["merged_variables"],
            )

            file_list.append(
                f"{dir_dict['frcst_high_reg_dir']}/{fnme_dict['frcst_high_reg_dir']}"
            )

        ds = xr.open_mfdataset(
            file_list,
            parallel=True,
            engine="netcdf4",
            autoclose=True,
            chunks={"time": 50},
        )

        coords = {
            "time": ds["time"].values,
            "ens": ds["ens"].values,
            "lat": ds["lat"].values.astype(np.float32),
            "lon": ds["lon"].values.astype(np.float32),
        }

        encoding = set_encoding(variable_config, coords, "lines")

        final_file = f"{dir_dict['frcst_high_reg_lnch_calib_dir']}/{fnme_dict['frcst_high_reg_lnch_calib_dir']}"

        try:
            ds.to_netcdf(final_file, encoding=encoding)
            logging.info("Calibrate forecast: successful")
        except:
            logging.error("Calibrate forecast: Something went wrong")
    else:
        for variable in variable_config:
            for year in range(syr, eyr + 1):
                # Update Filenames
                fnme_dict = dir_fnme.set_filenames(
                    domain_config,
                    syr,
                    eyr,
                    year,
                    month_str,
                    domain_config["raw_forecasts"]["merged_variables"],
                    variable,
                )

                file_list.append(
                    f"{dir_dict['frcst_high_reg_dir']}/{fnme_dict['frcst_high_reg_dir']}"
                )

            ds = xr.open_mfdataset(
                file_list,
                parallel=True,
                engine="netcdf4",
                autoclose=True,
                chunks={"time": 50},
            )

            coords = {
                "time": ds["time"].values,
                "ens": ds["ens"].values,
                "lat": ds["lat"].values.astype(np.float32),
                "lon": ds["lon"].values.astype(np.float32),
            }

            encoding = set_encoding(variable_config, coords, "lines")

            final_file = f"{dir_dict['frcst_high_reg_lnch_calib_dir']}/{fnme_dict['frcst_high_reg_lnch_calib_dir']}"

            try:
                ds.to_netcdf(final_file, encoding={variable: encoding[variable]})
                logging.info("Calibrate forecast: successful")
            except:
                logging.error("Calibrate forecast: Something went wrong")









@dask.delayed
def rechunk_reference(
    domain_config: dict,
    variable_config: dict,
    dir_dict: dict,
    year: int,
    month: int,
    variable: str,
):

    month_str = str(month).zfill(2)

    # if domain_config['reference_history']['merged_variables'] == True:
    # Update Filenames:
    #    fnme_dict = dir_fnme.set_filenames(domain_config, year, month_str,
    #                                       domain_config['reference_history']['merged_variables'])

    #    fle_string = f"{dir_dict['ref_high_reg_daily_dir']}/{fnme_dict['ref_high_reg_daily_dir']}"

    # ds = xr.open_mfdataset(input_file, parallel = True, chunks = {'time': 100})
    #    ds = xr.open_mfdataset(fle_string, parallel=True, chunks={'time': 50}, engine='netcdf4', preprocess=preprocess,

    #    coords = {'time': ds['time'].values, 'lat': ds['lat'].values.astype(np.float32), 'lon':
    # ds['lon'].values.astype(np.float32)}

    #    encoding = set_encoding(variable_config, coords, 'lines')

    ##   try:
    #        ds.to_netcdf(f"{dir_dict['ref_high_reg_daily_lnch_dir']}/
    # {fnme_dict['ref_high_reg_daily_lnch_dir']}", encoding=encoding)
    #    except:
    #        logging.error(f"Rechunk reference: Rechunking of reference data failed!")
    # else:
    #    for variable in variable_config:
    # Update Filenames:
    fnme_dict = dir_fnme.set_filenames(
        domain_config,
        year,
        month_str,
        domain_config["reference_history"]["merged_variables"],
        variable,
    )

    fle_string = (
        f"{dir_dict['ref_high_reg_daily_dir']}/{fnme_dict['ref_high_reg_daily_dir']}"
    )

    # ds = xr.open_mfdataset(input_file, parallel = True, chunks = {'time': 100})
    ds = xr.open_mfdataset(
        fle_string,
        parallel=True,
        chunks={"time": 50},
        engine="netcdf4",
        preprocess=preprocess,
        autoclose=True,
    )

    coords = {
        "time": ds["time"].values,
        "lat": ds["lat"].values.astype(np.float32),
        "lon": ds["lon"].values.astype(np.float32),
    }

    encoding = set_encoding(variable_config, coords, "lines")

    try:
        ds.to_netcdf(
            f"{dir_dict['ref_high_reg_daily_lnch_dir']}/{fnme_dict['ref_high_reg_daily_lnch_dir']}",
            encoding={variable: encoding[variable]},
        )
    except:
        logging.error(
            f"Rechunk reference: Rechunking of reference data failed for variable {variable}!"
        )


@dask.delayed
def calib_reference(
    domain_config: dict,
    variable_config: dict,
    dir_dict: dict,
    syr: int,
    eyr: int,
    variable: str,
):

    fle_list = []

    # if domain_config['reference_history']['merged_variables'] == True:
    #    for year in range(syr, eyr + 1):
    #        # Update filenames
    #        month_str = "01"  # dummy
    #        fnme_dict = dir_fnme.set_filenames(domain_config, year, month_str, domain_config
    # ['reference_history']['merged_variables'])#

    #        fle_list.append(f"{dir_dict['ref_high_reg_daily_dir']}/{fnme_dict['ref_high_reg_daily_dir']}")

    #    # ds = xr.open_mfdataset(input_file, parallel = True, chunks = {'time': 100})
    #    ds = xr.open_mfdataset(fle_list, parallel=True, chunks={'time': 50}, engine='netcdf4', autoclose=True)

    #    coords = {'time': ds['time'].values, 'lat': ds['lat'].values.astype(np.float32),
    #              'lon': ds['lon'].values.astype(np.float32)}

    #    encoding = set_encoding(variable_config, coords, 'lines')

    #    try:
    #        ds.to_netcdf(
    #            f"{dir_dict['ref_high_reg_daily_lnch_calib_dir']}/{fnme_dic
    # t['ref_high_reg_daily_lnch_calib_dir']}",
    #            encoding=encoding)
    #    except:
    #        logging.error(f"Rechunk reference: Rechunking of reference data failed for variable!")

    # else:

    #    for variable in variable_config:

    for year in range(syr, eyr + 1):
        # Update filenames
        month_str = "01"  # dummy
        fnme_dict = dir_fnme.set_filenames(
            domain_config,
            year,
            month_str,
            domain_config["reference_history"]["merged_variables"],
            variable,
        )

        fle_list.append(
            f"{dir_dict['ref_high_reg_daily_lnch_dir']}/{fnme_dict['ref_high_reg_daily_lnch_dir']}"
        )

        # ds = xr.open_mfdataset(input_file, parallel = True, chunks = {'time': 100})

    ds = xr.open_mfdataset(fle_list, parallel=True, engine="netcdf4", autoclose=True)

    coords = {
        "time": ds["time"].values,
        "lat": ds["lat"].values.astype(np.float32),
        "lon": ds["lon"].values.astype(np.float32),
    }

    encoding = set_encoding(variable_config, coords, "lines")

    try:
        ds.to_netcdf(
            f"{dir_dict['ref_high_reg_daily_lnch_calib_dir']}/{fnme_dict['ref_high_reg_daily_lnch_calib_dir']}",
            encoding={variable: encoding[variable]},
        )
    except:
        logging.error(
            f"Rechunk reference: Rechunking of reference data failed for variable {variable}!"
        )

