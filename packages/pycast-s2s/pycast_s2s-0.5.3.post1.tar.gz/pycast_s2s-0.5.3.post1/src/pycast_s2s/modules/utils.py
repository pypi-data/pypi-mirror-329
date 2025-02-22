# import packages
import datetime as dt
import os
import sys
from pathlib import Path
from subprocess import PIPE, run
import logging
import numpy as np
import pandas as pd

import eccodes
import cfgrib
import xarray as xr
import zarr
import json



def set_and_make_dirs(domain_config: dict) -> dict:
    """ Prepare directory names

    For running the whole BCSD-workflow, we need to set various directories for all the different
    processing steps. 

    Parameters
    ----------
    domain_config : dict
        A dictionary with all information about the current domain

    Returns
    -------
    reg_dir_dict
        A dictionary with all required directories for the regional processing stels
    glob_dir_dict
        A dictionary which contains the directories of the global data; this needs to be
        made more flexible in a future release...
    """
    
    storage = 'beegfs'

    reg_dir_dict = {"domain_dir": f"{domain_config['regroot']}"}
    # Then the level 1 directories
    reg_dir_dict["static_dir"] = f"{reg_dir_dict['domain_dir']}/00_static/"
    reg_dir_dict[
        "raw_forecasts_dir"
    ] = f"{reg_dir_dict['domain_dir']}/01_raw_forecasts/"
    reg_dir_dict["reference_dir"] = f"{reg_dir_dict['domain_dir']}/02_reference/"
    reg_dir_dict["processed_dir"] = f"{reg_dir_dict['domain_dir']}/03_processed/"
    reg_dir_dict["aggregated_dir"] = f"{reg_dir_dict['domain_dir']}/04_aggregated/"
    reg_dir_dict[
        "forecast_measure_dir"
    ] = f"{reg_dir_dict['domain_dir']}/05_forecast_measures/"

    # Then the level 2 directories
    reg_dir_dict[
        "raw_forecasts_initial_resolution_dir"
    ] = f"{reg_dir_dict['raw_forecasts_dir']}initial_resolution/"
    reg_dir_dict[
        "raw_forecasts_target_resolution_dir"
    ] = f"{reg_dir_dict['raw_forecasts_dir']}target_resolution/"
    reg_dir_dict[
        "raw_forecasts_zarr_dir"
    ] = f"{reg_dir_dict['raw_forecasts_dir']}zarr_stores/"
    reg_dir_dict[
        "reference_initial_resolution_dir"
    ] = f"{reg_dir_dict['reference_dir']}initial_resolution"
    reg_dir_dict[
        "bcsd_forecast_zarr_dir"
    ] = f"{reg_dir_dict['processed_dir']}zarr_stores/"
    reg_dir_dict[
        "reference_target_resolution_dir"
    ] = f"{reg_dir_dict['reference_dir']}target_resolution/"
    reg_dir_dict["reference_zarr_dir"] = f"{reg_dir_dict['reference_dir']}zarr_stores/"

    reg_dir_dict["climatology_dir"] = f"{reg_dir_dict['aggregated_dir']}/climatology/"
    reg_dir_dict["monthly_dir"] = f"{reg_dir_dict['aggregated_dir']}/monthly/"
    reg_dir_dict["statistic_dir"] = f"{reg_dir_dict['aggregated_dir']}/statistic/"


    # Then the level 3 directories
    reg_dir_dict[
        "bcsd_forecast_mon_zarr_dir"
    ] = f"{reg_dir_dict['monthly_dir']}zarr_stores_bcsd/"
    reg_dir_dict[
        "ref_forecast_mon_zarr_dir"
    ] = f"{reg_dir_dict['monthly_dir']}zarr_stores_ref/"
    reg_dir_dict[
        "seas_forecast_mon_zarr_dir"
    ] = f"{reg_dir_dict['monthly_dir']}zarr_stores_seas/"

    # If not yet done so, create all project directories

    if storage == 's3':
        print('S3 chosen')
    else:
        for key in reg_dir_dict:
            if not os.path.isdir(reg_dir_dict[key]):
                print(f"Creating directory {reg_dir_dict[key]}")
                os.makedirs(reg_dir_dict[key])

    glob_dir_dict = {
        "global_forecasts": "/bg/data/s2s/raw_downloads/global",
        "global_reference": "/pd/data/regclim_data/gridded_data/reanalyses/era5_land/daily",
        "global_reforecasts": "/pd/data/regclim_data/gridded_data/seasonal_predictions/seas5/daily",
    }
    return reg_dir_dict, glob_dir_dict


def update_global_attributes(global_config, bc_params, coords, domain):
    """ Add information about the current workflow to the output NetCDFs

    The global attributes of the output NetCDFs should contain some information about the current
    domain and the parameters of the bias-correction. This function reads the respective information
    from the different parameter dictionaries and updates the global attributes accordingly. 

    Parameters
    ----------
    global_config : dict
        A dictionary with all global attributes for the NetCDFs
    bc_params: dict
        A dictionary that holds the settings for the bias correction
    coords: dict
        A dictionary with the coordinates of the output NetCDFs
    domain: str
        The name of the current domain
        
    Returns
    -------
    global_config
        A dictionary with global attributes for the output NetCDFs
    """
    
    # Update the global attributes with some run-specific parameters
    now = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    global_config["comment"] = f"Domain: {domain}"
    
    if bc_params is not None:
        global_config["comment"] = global_config["comment"] + f"BCSD-Parameter: {str(bc_params)}"
        
    global_config["creation_date"] = f"{now}"

    global_config["geospatial_lon_min"] = min(coords["lon"])
    global_config["geospatial_lon_max"] = max(coords["lon"])
    global_config["geospatial_lat_min"] = min(coords["lat"])
    global_config["geospatial_lat_max"] = max(coords["lat"])
    global_config["StartTime"] = pd.to_datetime(coords["time"][0]).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )
    global_config["StopTime"] = pd.to_datetime(coords["time"][-1]).strftime(
        "%Y-%m-%dT%H:%M:%S"
    )

    return global_config


def set_input_files(
    domain_config: dict, reg_dir_dict: dict, month: int, year: int, variable: str
):
    """
    Generate file paths for input data based on configuration and time information.

    Parameters
    ----------
    domain_config : dict
        Dictionary containing configuration parameters for the domain.
    reg_dir_dict : dict 
        Dictionary containing directory paths for different types of files.
    month : int 
        Numeric representation of the month (1 to 12).
    year : int
        Year for which the input files are generated.
    variable : str 
        Variable for which the input files are generated.

    Returns
    -------
    raw_full : str
        File path for raw forecasts
    pp_full : str
        File path for processed forecasts
    refrcst_full : str
        File path for calibrated raw forecasts
    ref_full : str 
        File path for reference data
    
    Example:

    .. code-block:: python

        domain_config = {...}  # Dictionary with domain configuration parameters
        reg_dir_dict = {...}   # Dictionary with directory paths
        month = 3
        year = 2023
        variable = "temperature"

        raw_file, pp_file, refrcst_zarr, ref_zarr = set_input_files(domain_config, reg_dir_dict, month, year, variable)

    The function constructs file paths for different types of input data based on the provided parameters. The generated file paths include:
    - `raw_full`: Path to the raw forecasts NetCDF file.
    - `pp_full`: Path to the processed forecasts NetCDF file.
    - `refrcst_full`: Path to the calibrated raw forecasts Zarr file.
    - `ref_full`: Path to the reference data Zarr file.

    Note:
    - The function uses configuration parameters from `domain_config` and directory paths from `reg_dir_dict` to construct file paths.
    - The `month` and `year` parameters determine the time period for which the files are generated.
    - The `variable` parameter specifies the variable for which the input files are generated.
    """

    raw_file = f"{domain_config['variable_mapping'][variable]['forecasts']['product_prefix']}_{variable}_{year}{month:02d}_{domain_config['target_resolution']}.nc"
    raw_full = f"{reg_dir_dict['raw_forecasts_target_resolution_dir']}{raw_file}"

    pp_file = f"{domain_config['bcsd_forecasts']['prefix']}_v{domain_config['version']}_{variable}_{year}{month:02d}_{domain_config['target_resolution']}.nc"
    pp_full = f"{reg_dir_dict['processed_dir']}{pp_file}"

    refrcst_zarr = f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{month:02d}_{domain_config['target_resolution']}_calib_linechunks.zarr"
    refrcst_full = f"{reg_dir_dict['raw_forecasts_zarr_dir']}{refrcst_zarr}"

    ref_zarr = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{domain_config['target_resolution']}_calib_linechunks.zarr"
    ref_full = f"{reg_dir_dict['reference_zarr_dir']}{ref_zarr}"

    return raw_full, pp_full, refrcst_full, ref_full


def set_encoding(variable_config, coordinates, type="maps"):
    """ Prepares an encoding-dictionary 

    When writing data to NetCDF-files, we need to set some parameters that can substantially
    imact the I/O-performance as well as the filesize. A standard set of parameters is defined
    with this little function.

    Parameters
    ----------
    variable_config : dict
        A dictionary with all the variables that will be processed during the current workflw
    coordinates : dict
        A dictionary that holds the coordinates of the data for which we need encoding parameter. 
    type: str
        Can be set to "maps" or "lines" for defining the chunking of the output data; map-chunks
        imporove the performance when whole maps are needed while line-chunks work much better if
        data along the time-axis is required.

    Returns
    -------
    encoding
        A dictionary with the variables from variable_config and the corresponding parameter that 
        will be used for writing the NetCDF-files
    """

    if type == "lines":
        chunksizes = (
            [len(coordinates["time"]), len(coordinates["ens"]), 1, 1]
            if "ens" in coordinates
            else [len(coordinates["time"]), 1, 1]
        )
    elif type == "maps":
        chunksizes = (
            [
                20,
                len(coordinates["ens"]),
                len(coordinates["lat"]),
                len(coordinates["lon"]),
            ]
            if "ens" in coordinates
            else [20, len(coordinates["lat"]), len(coordinates["lon"])]
        )
    encoding = {
        variable: {
            "zlib": True,
            "complevel": 1,
            "_FillValue": variable_config[variable]["_FillValue"],
            "scale_factor": variable_config[variable]["scale_factor"],
            "add_offset": variable_config[variable]["add_offset"],
            "dtype": variable_config[variable]["dtype"],
            "chunksizes": chunksizes,
        }
        for variable in variable_config
    }
    encoding['lat'] = {"_FillValue": None, "dtype": "float"}
    encoding['lon'] = {"_FillValue": None, "dtype": "float"}
    encoding['time'] = {"_FillValue": None, "units": 'days since 1950-01-01 00:00:00', "dtype": "int32"}

    if "ens" in coordinates:
        encoding['ens'] = {"dtype": "int16"}

    return encoding


def set_zarr_encoding(variable_config):
    """
    Generate Zarr encoding configuration for variables based on provided variable configurations.

    Parameters
    ----------
    variable_config : dict
        Dictionary containing variable-specific configuration parameters.

    Returns
    -------
    encoding: dict 
        Dictionary containing Zarr encoding configurations for each variable.

    Example:

    .. code-block:: python

        variable_config = {
            "temperature": {"_FillValue": -9999, "scale_factor": 1.0, "add_offset": 0.0, "dtype": "float32"},
            "precipitation": {"_FillValue": -9999, "scale_factor": 1.0, "add_offset": 0.0, "dtype": "float32"},
        }

        encoding = set_zarr_encoding(variable_config)

    The function constructs Zarr encoding configurations for each variable based on the provided `variable_config` dictionary.
    The generated encoding dictionary includes compression settings and other metadata for each variable, as well as default configurations for 'lat', 'lon', and 'time' variables.

    Note:
    - The function iterates through each variable in `variable_config` and generates an encoding configuration based on specified parameters.
    - Default encoding configurations for 'lat', 'lon', and 'time' variables are also included.
    """

    encoding = {}

    for variable in variable_config:

        encoding[variable] = {
            "compressor": zarr.Blosc(cname="zstd", clevel=3, shuffle=2),
            "_FillValue": variable_config[variable]["_FillValue"],
            "scale_factor": variable_config[variable]["scale_factor"],
            "add_offset": variable_config[variable]["add_offset"],
            "dtype": variable_config[variable]["dtype"],
        }
        
        encoding['lat'] = {"_FillValue": None, "dtype": "float"}
        encoding['lon'] = {"_FillValue": None, "dtype": "float"}
        encoding['time'] = {"_FillValue": None, "units": 'days since 1950-01-01 00:00:00', "dtype": "float"}

    return encoding


def create_4d_netcdf(
    file_out, global_config, domain_config, variable_config, coordinates, variable
    ) -> xr.Dataset:
    """
    Create a 4D NetCDF dataset with specified metadata and coordinates.

    Parameters
    ----------
    file_out : str 
        The path to the output NetCDF file.
    global_config : dict   
        Global attributes for the NetCDF file.
    domain_config : dict
        Domain-specific configuration.
    variable_config : dict
        Variable-specific configuration containing standard_name, long_name, and units.
    coordinates : dict
        Dictionary containing coordinate arrays for time, ens (ensemble), lat (latitude), and lon (longitude).
    variable : dict
        Name of the variable for which the NetCDF dataset is created.

    Returns
    -------
    ds : xr.Dataset 
        A 4D xarray Dataset with the specified variable, dimensions, coordinates, and attributes.

    Example:
    
    .. code-block:: python

        file_out = "output.nc"
        global_config = {"history": "Created by create_4d_netcdf function"}
        domain_config = {...}  # Domain-specific configuration
        variable_config = {
            "temperature": {"standard_name": "air_temperature", "long_name": "Temperature", "units": "K"}
        }
        coordinates = {
            "time": pd.date_range("2023-01-01", periods=10, freq="D"),
            "ens": np.arange(1, 6),
            "lat": np.linspace(-90, 90, 180),
            "lon": np.linspace(-180, 180, 360),
        }
        variable = "temperature"

        ds = create_4d_netcdf(file_out, global_config, domain_config, variable_config, coordinates, variable)

    The function generates an xarray Dataset with a DataArray for the specified variable.
    The coordinates dictionary should contain arrays for "time," "ens," "lat," and "lon."
    The variable_config dictionary should contain metadata information for the specified variable.
    The resulting dataset can be written to a NetCDF file using ds.to_netcdf() method (currently commented out in the code).
    """
    encoding = set_encoding(variable_config, coordinates)

    da_dict = {
        variable: xr.DataArray(
            None,
            dims=["time", "ens", "lat", "lon"],
            coords={
                "time": (
                    "time",
                    coordinates["time"],
                    {"standard_name": "time", "long_name": "time"},
                ),
                "ens": (
                    "ens",
                    coordinates["ens"],
                    {
                        "standard_name": "realization",
                        "long_name": "ensemble_member",
                    },
                ),
                "lat": (
                    "lat",
                    coordinates["lat"],
                    {
                        "standard_name": "latitude",
                        "long_name": "latitude",
                        "units": "degrees_north",
                    },
                ),
                "lon": (
                    "lon",
                    coordinates["lon"],
                    {
                        "standard_name": "longitude",
                        "long_name": "longitude",
                        "units": "degrees_east",
                    },
                ),
            },
            attrs={
                "standard_name": variable_config[variable]["standard_name"],
                "long_name": variable_config[variable]["long_name"],
                "units": variable_config[variable]["units"],
            },
        )
    }
    return xr.Dataset(
        data_vars={variable: da_dict[variable]},
        coords={
            "time": (
                "time",
                coordinates["time"],
                {"standard_name": "time", "long_name": "time"},
            ),
            "ens": (
                "ens",
                coordinates["ens"],
                {
                    "standard_name": "realization",
                    "long_name": "ensemble_member",
                },
            ),
            "lat": (
                "lat",
                coordinates["lat"],
                {
                    "standard_name": "latitude",
                    "long_name": "latitude",
                    "units": "degrees_north",
                },
            ),
            "lon": (
                "lon",
                coordinates["lon"],
                {
                    "standard_name": "longitude",
                    "long_name": "longitude",
                    "units": "degrees_east",
                },
            ),
        },
        attrs=global_config,
    )



def get_coords(filename: str, filetype: str = "netcdf") -> dict:
    """Retrieves coordinates from a forecast or reference file.

    This function extracts time, latitude, and longitude coordinates from a file.
    If the file is a forecast file (NetCDF or GRIB), it also extracts the ensemble coordinate.

    Args:
        filename (str): Path to the file.
        filetype (str, optional): Type of the file ('netcdf' or 'grib'). Defaults to 'netcdf'.

    Returns:
        dict: A dictionary containing the extracted coordinates.
    """

    coords = {}
    if filetype == "netcdf":
        ds = xr.open_dataset(filename, engine="netcdf4")
        coords["time"] = ds["time"].values
        coords["lat"] = ds["lat"].values
        coords["lon"] = ds["lon"].values
        if "ens" in ds.dims:  # Check for ensemble dimension
            coords["ens"] = ds["ens"].values
    elif filetype == "grib":
        ds = cfgrib.open_dataset(filename, indexpath="")
        coords["time"] = ds["step"].values
        coords["lat"] = ds["latitude"].values
        coords["lon"] = ds["longitude"].values
        if "number" in ds.dims:  # Check for ensemble dimension (number in GRIB)
            coords["ens"] = ds["number"].values

    return coords

# def get_coords_from_frcst(filename, filetype='netcdf'):
#     """Retrieves coordinates from a forecast file.

#     This function extracts time, latitude, longitude, and ensemble coordinates from a
#     forecast file, supporting both NetCDF and GRIB formats.

#     Parameters
#     ----------
#     filename : str
#         Path to the forecast file.
#     filetype : str 
#         (Optional) Type of the forecast file ('netcdf' or 'grib'). Defaults to 'netcdf'.

#     Returns
#     -------
#     coords: dict
#         A dictionary containing the extracted coordinates.
#     """
    
#     if filetype=='netcdf':
#         ds = xr.open_dataset(filename, engine = "netcdf4")
#         coords = {
#             "time": ds["time"].values,
#             "lat": ds["lat"].values,
#             "lon": ds["lon"].values,
#             "ens": ds["ens"].values,
#         }
#     elif filetype=='grib':
#         ds = cfgrib.open_dataset(filename, indexpath='')
#         coords = {
#             "time": ds["step"].values,
#             "lat": ds["latitude"].values,
#             "lon": ds["longitude"].values,
#             "ens": ds["number"].values,
#         }

#     return coords


# def get_coords_from_ref(filename):
#     """Retrieves coordinates from a reference file.

#     This function extracts time, latitude, and longitude coordinates from a reference file.

#     Parameters
#     ----------
#     filename : str
#         Path to the reference file.

#     Returns
#     -------
#     dict: dict
#         A dictionary containing the extracted coordinates.
#     """
#     ds = xr.open_dataset(filename)

#     # return {
#     #    'time': ds['time'].values,
#     #    'lat': ds['lat'].values.astype(np.float32),
#     #    'lon': ds['lon'].values.astype(np.float32),
#     #    'ens': ds['ens'].values
#     # }

#     return {
#         "time": ds["time"].values,
#         "lat": ds["lat"].values,
#         "lon": ds["lon"].values,
#     }


def preprocess_mdl_hist(filename, month, variable):
    """Preprocesses model history data by creating a consistent time dimension.

    This function takes model history data with separate 'year' and 'time' dimensions
    and combines them into a single 'time' dimension with datetime values. It assumes
    the input data has monthly chunks and processes a specific variable within the dataset.

    Parameters
    ----------
    filename : str
        Path to the model history NetCDF file.
    month : int 
        The month for which to process the data (1-12).
    variable : str 
        The name of the variable to extract and process.

    Returns
    -------
    xr.Dataset : xr.Dataset
        The preprocessed dataset with a unified 'time' dimension.
    """
    ds = xr.open_mfdataset(
        filename,
        chunks={"time": 215, "year": 36, "ens": 25, "lat": 10, "lon": 10},
        parallel=True,
        engine="netcdf4",
    )

    ds = ds[variable]

    # Define time range
    year_start = ds.year.values[0].astype(int)
    year_end = ds.year.values[-1].astype(int)
    nday = len(ds.time.values)

    # Create new time based on day and year
    da_date = da.empty(shape=0, dtype=np.datetime64)
    for yr in range(year_start, year_end + 1):
        date = np.asarray(
            pd.date_range(f"{yr}-{month}-01 00:00:00", freq="D", periods=nday)
        )
        da_date = da.append(da_date, date)

    return (
        ds.stack(date=("year", "time"))
        .assign_coords(date=da_date)
        .rename(date="time")
    )


def run_cmd(cmd, path_extra=Path(sys.exec_prefix) / "bin"):
    """Runs a bash command.

    This function executes a bash command using the subprocess module. It extends the
    environment's PATH variable with an additional path and raises a RuntimeError if the
    command fails.

    Parameters
    ----------
    cmd : list 
        The bash command as a list of strings.
    path_extra : Path 
        (Optional) Additional path to add to the PATH environment variable. Defaults to Path(sys.exec_prefix) / "bin".

    Returns
    -------
    str: str
        The standard output of the command.

    Raises
    -------
        RuntimeError: If the command fails (non-zero return code).
    """
    # '''Run a bash command.'''
    env_extra = os.environ.copy()
    env_extra["PATH"] = f"{str(path_extra)}:" + env_extra["PATH"]
    status = run(cmd, check=False, stderr=PIPE, stdout=PIPE, env=env_extra)
    if status.returncode != 0:
        error = f"""{' '.join(cmd)}: {status.stderr.decode('utf-8')}"""
        raise RuntimeError(f"{error}")
    return status.stdout.decode("utf-8")


def decode_processing_years(years_string):
    """Decodes a string of years into a list of years for processing.

    This function takes a comma-separated string of years and converts it into a list of integers.
    It handles different input formats: single year, start and end year, or a sequence of years.

    Parameters
    ----------
    years_string : str 
        A comma-separated string of years.

    Returns
    -------
    years : list 
        A list of years to process.
    """

    year_list = [int(item) for item in years_string.split(",")]

    if len(year_list) == 1:
        # We want to run the routine for a single year
        years = [year_list[0]]
    elif len(year_list) == 2:
        years = year_list
    elif len(year_list) == 3:
        if year_list[1] == 0:
            years = range(
                year_list[0], year_list[2] + 1
            )  # We want the last year to be included in the list...
        else:
            years = year_list
    elif len(year_list) > 3:
        years = year_list

    return years


def decode_processing_months(months_string):
    """Decodes a string of months into a list of months for processing.

    This function takes a comma-separated string of months and converts it into a list of integers.
    It handles different input formats: single month, start and end month, or a sequence of months.

    Parameters
    ----------
    months_string : str 
        A comma-separated string of months.

    Returns
    -------
    months : list 
        A list of months to process.
    """

    month_list = [int(item) for item in months_string.split(",")]

    if len(month_list) == 1:
        # We want to run the routine for a single year
        months = [month_list[0]]
    elif len(month_list) == 2:
        months = month_list
    elif len(month_list) == 3:
        if month_list[1] == 0:
            months = range(
                month_list[0], month_list[2] + 1
            )  # We want the last month to be included in the list...
        else:
            months = month_list
    elif len(month_list) > 3:
        months = month_list

    return months


# Get the absolute path of the conf/ directory
def load_json(filename):
    """Load JSON data from a file, searching in configured locations.

    This function attempts to load JSON data from a file named `filename`. It searches for the file in the following locations:

    1. The directory specified by the environment variable `PYCAST_S2S_CONFIG`.
    2. The `conf/` directory in the current working directory.

    Args:
        filename (str): The name of the JSON file to load.

    Returns:
        dict or list: The loaded JSON data as a Python dictionary or list.

    Raises:
        FileNotFoundError: If the file is not found in any of the searched locations.
    """
    config_dir = os.environ.get("PYCAST_S2S_CONFIG")
    search_paths = []
    if config_dir:
        search_paths.append(Path(config_dir) / filename)
    search_paths.append(Path("./conf/") / filename)  # Default fallback

    for path in search_paths:
        if path.exists():
            with open(path, "r") as j:
                return json.load(j)

    logging.error(f"Configuration file {filename} not found in any configured location.")
    raise FileNotFoundError(f"Configuration file {filename} is missing.")



# def load_json(filename):
#     CONF_DIR = Path(__file__).parents[1] / "conf"
    
#     """Load a JSON config file from the conf directory."""
#     file_path = CONF_DIR / filename
#     if not file_path.exists():
#         raise FileNotFoundError(f"Configuration file {filename} not found in {CONF_DIR}")
    
#     with open(file_path, "r", encoding="utf-8") as f:
#         return json.load(f)
    
    

# def load_config(file_path):
#     """Load JSON data from a file.

#     This function reads JSON data from the specified file path and returns it as a Python object.
#     It raises a FileNotFoundError if the file does not exist.

#     Parameters
#     ----------
#     file_path : str 
#         The path to the JSON file.

#     Returns
#     -------
#     dict or list : dict or list
#         The loaded JSON data as a Python dictionary or list.

#     Raises
#     -------
#         FileNotFoundError: If the file specified by `file_path` does not exist.
#     """
#     if not os.path.exists(file_path):
#         logging.error(f"Configuration file {file_path} not found.")
#         raise FileNotFoundError(f"Configuration file {file_path} is missing.")
#     with open(file_path, "r") as j:
#         return json.load(j)

