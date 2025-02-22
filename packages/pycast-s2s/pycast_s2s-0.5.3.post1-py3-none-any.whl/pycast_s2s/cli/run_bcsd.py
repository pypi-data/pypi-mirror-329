"""
Applies bias correction to regional climate forecasts using the BCSD method.

This script performs bias correction on regional climate forecasts using the Bias Correction Spatial Disaggregation (BCSD) method.
It takes raw forecast data, reforecasts, and observational reference data as input and produces bias-corrected forecasts.
The script supports various configuration options, including domain selection, processing years and months, variable selection, and cross-validation.
It utilizes Dask for parallel processing and Xarray for handling NetCDF and Zarr data formats.
"""

# import packages
import argparse
import json
import logging
import pandas as pd
import dask
import numpy as np
import xarray as xr
from tqdm import tqdm
from dask.distributed import Client
import os

from pycast_s2s.modules import helper_modules
from pycast_s2s.modules import cluster_modules
from pycast_s2s.modules.bc_module import bc_module
from pycast_s2s.modules.logger_setup import setup_logger

# Initialize logger
logger = setup_logger(log_name="bcsd_pipeline", log_level="INFO")


def get_clas():
    # insert period, for which the bcsd-should be running! similar to process_regional_forecast
    parser = argparse.ArgumentParser(
        description="Python-based BCSD",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-d", "--domain", action="store", type=str, help="Domain", required=True
    )

    parser.add_argument(
        "-Y",
        "--Years",
        action="store",
        type=str,
        help="Years for which the processing should be executed",
        required=False,
    )

    parser.add_argument(
        "-M",
        "--Months",
        action="store",
        type=str,
        help="Months for which the processing should be executed",
        required=False,
    )
    
    parser.add_argument(
        "-H",
        "--Horizon",
        action="store",
        type=int,
        help="Number of time-steps that should be bias-corrected",
        required=False,
    )



    parser.add_argument(
        "-v", "--variables",
        type=lambda s: s.split(","),  # Convert comma-separated string into a list
        help="Comma-separated list of variables",
    )

    parser.add_argument(
        "-c", "--crossval",
        action="store_true",
        help="If set, do not use actual forecast for computing forecast climatology"
    )

    parser.add_argument(
        "-s",
        "--forecast_structure",
        action="store",
        type=str,
        help="Structure of the line-chunked forecasts (can be 5D or 4D)",
        required=False,
    )

    parser.add_argument(
        "-N",
        "--nodes",
        action="store",
        type=int,
        help="Number of nodes for running the code",
        required=False,
    )

    parser.add_argument(
        "-n",
        "--ntasks",
        action="store",
        type=int,
        help="Number of tasks / CPUs",
        required=False,
    )

    parser.add_argument(
        "-p",
        "--partition",
        action="store",
        type=str,
        help="Partition to which we want to submit the job",
        required=False,
    )

    parser.add_argument(
        "-f",
        "--scheduler_file",
        action="store",
        type=str,
        help="""If a scheduler-file is provided, the function does not start its own cluster 
            but rather uses a running environment""",
        required=False,
    )
    
    # A
    parser.add_argument("--raw_forecast", type=str, help="Path to raw forecast file", required=False)
    parser.add_argument("--bc_forecast", type=str, help="Path to post-processed file", required=False)
    parser.add_argument("--reforecasts", type=str, help="Path to reference forecast file", required=False)
    parser.add_argument("--reference", type=str, help="Path to observational reference file", required=False)
    
    
    return parser.parse_args()

# Function to check if a date falls within the window, handling year boundaries
def within_window(time, start_window, end_window):
    """Check if a date falls within a defined time window, handling year boundaries.

    This function determines if a given date falls within a time window defined by
    `start_window` and `end_window`, correctly handling cases where the window
    spans across the end of a year and the beginning of the next.

    Args:
        time: The date to check, represented as a pandas Timestamp.

    Returns:
        True if the date falls within the window, False otherwise.
    """
    time = pd.Timestamp(time)
    ref_month, ref_day = time.month, time.day
    start_month, start_day = start_window.month, start_window.day
    end_month, end_day = end_window.month, end_window.day
    
    # Normal case: Within the same year (e.g., June 5 ± 10 days)
    if (start_month, start_day) <= (end_month, end_day):
        return (start_month, start_day) <= (ref_month, ref_day) <= (end_month, end_day)
    
    # Year-boundary case: Spanning December-January (e.g., December 25 ± 10 days)
    else:
        return (ref_month, ref_day) >= (start_month, start_day) or (ref_month, ref_day) <= (end_month, end_day)


def main():       
    logger.info("Starting BCSD Pipeline")

    logger.info(f"[run_bcsd] ----------------------------------")
    logger.info(f"[run_bcsd]       Pycast S2S Main program     ")
    logger.info(f"[run_bcsd] ----------------------------------")
    logger.info(f"[run_bcsd]             Version 0.1           ")
    logger.info(f"[run_bcsd] ----------------------------------")

    # Read the command line arguments
    args = get_clas()

    logger.info(f"Processing domain: {args.domain}, Years: {args.Years}, Months: {args.Months}")

    # Load the config files
    try:
        domain_config = helper_modules.load_json("conf/domain_config.json")
        attribute_config = helper_modules.load_json("conf/attribute_config.json")
        variable_config = helper_modules.load_json("conf/variable_config.json")
        logger.info("Loaded configuration files successfully")
    except FileNotFoundError as e:
        logger.error(f"Configuration file missing: {e}")
        exit(1)

    # Check
    if args.domain not in domain_config:
        logger.error(f"No configuration found for domain {args.domain}")
        exit(1)  # Exit the program gracefully
    else:
        domain_config = domain_config[args.domain]


    if args.variables is not None:
        variable_config = {
            key: value
            for key, value in variable_config.items()
            if key in args.variables
        }
    else:
        variable_config = {
            key: value
            for key, value in variable_config.items()
            if key in domain_config["variables"]
        }

    if args.raw_forecast and args.bc_forecast and args.reference and args.reforecasts:
        reg_dir_dict = {}
        glob_dir_dict = {}
    else:
        reg_dir_dict, glob_dir_dict = helper_modules.set_and_make_dirs(domain_config)


    if args.raw_forecast is not None:
        process_months = [None]
        process_years = [None]
    else:
        process_years = helper_modules.decode_processing_years(args.Years)
        if args.Months is not None:
            process_months = helper_modules.decode_processing_months(args.Months)
        else:
            process_months = range(1,13)

    #process_years = helper_modules.decode_processing_years(args.Years)

    #if args.Months is not None:
    #    process_months = helper_modules.decode_processing_months(args.Months)

    if args.reforecasts is not None:
        syr_calib = domain_config["syr_calib"]
        eyr_calib = domain_config["eyr_calib"]

    if args.partition and args.scheduler_file:
        logger.error("Cannot specify both --partition and --scheduler_file. Choose one.")
        exit(1)

    # Get some ressourcers
    if args.partition is not None:
        client, cluster = cluster_modules.getCluster(
            args.partition, args.nodes, args.ntasks
        )

        client.get_versions(check=True)
        client.amm.start()

        logger.info(f"[run_bcsd] Dask dashboard available at {client.dashboard_link}")

    if args.scheduler_file is not None:
        client = Client(scheduler_file=args.scheduler_file)

        client.get_versions(check=True)
        client.amm.start()

        logger.info(f"[run_bcsd] Dask dashboard available at {client.dashboard_link}")

    # Insert IF-Statement in order to run the bcsd for the historical files
    for year in process_years:

        for month in process_months:

            for variable in variable_config:
                if year is None and month is None:
                    logger.info(f"[run_bcsd] Starting BC-routine with pre-defined filenames and variable {variable}")
                else:
                    logger.info(f"[run_bcsd] Starting BC-routine for year {year}, month {month} and variable {variable}")

                # Use filenames from CLI if provided, otherwise generate them
                if args.raw_forecast and args.bc_forecast and args.reference and args.reforecasts:
                    raw_full = args.raw_forecast
                    pp_full = args.bc_forecast
                    refrcst_full = args.reforecasts
                    ref_full = args.reference
                    logger.info("[run_bcsd] Using filenames provided via command line.")
                else:
                    raw_full, pp_full, refrcst_full, ref_full = helper_modules.set_input_files(
                        domain_config, reg_dir_dict, month, year, variable
                    )
                    logger.info("[run_bcsd] Using automatically generated filenames.")

                coords = helper_modules.get_coords_from_frcst(raw_full)

                global_attributes = helper_modules.update_global_attributes(
                    attribute_config, domain_config["bc_params"], coords, args.domain
                )

                encoding = helper_modules.set_encoding(variable_config, coords)

                ds = helper_modules.create_4d_netcdf(
                    pp_full,
                    global_attributes,
                    domain_config,
                    variable_config,
                    coords,
                    variable,
                )

                logger.info(f"Using {ref_full} as reference for the calibration period")
                logger.info(f"Using {refrcst_full} as forecasts for the calibration period")
                logger.info(f"Using {raw_full} as actual forecasts")

                if ref_full.endswith(".zarr"):
                    ds_obs = xr.open_zarr(ref_full, consolidated=False)
                    ds_obs = xr.open_zarr(
                        ref_full,
                        chunks={"time": len(ds_obs.time), "lat": 10, "lon": 10},
                        consolidated=False
                    )                                            
                elif ref_full.endswith(".nc"):
                    ds_obs = xr.open_dataset(ref_full, engine='netcdf4')
                    da_obs = ds_obs[variable].persist()

                    #with xr.open_dataset(ref_full, engine='netcdf4') as ds_obs:
                    #    da_obs = ds_obs[args.variables].persist()

                if args.forecast_structure == "5D":
                    ds_mdl = helper_modules.preprocess_mdl_hist(
                        refrcst_full, month, variable
                    )
                    da_mdl = ds_mdl.persist()
                elif args.forecast_structure == "4D":

                    if refrcst_full.endswith(".zarr"):
                        ds_mdl = xr.open_zarr(refrcst_full, consolidated=False)
                        ds_mdl = xr.open_zarr(
                            refrcst_full,
                            chunks={
                                "time": len(ds_mdl.time),
                                "ens": len(ds_mdl.ens),
                                "lat": 'auto',
                                "lon": 'auto',
                            },
                            consolidated=False
                        )
                    elif refrcst_full.endswith(".nc"):
                        #with xr.open_dataset(refrcst_full, engine='netcdf4') as ds_mdl:
                        #    da_mdl = ds_mdl[args.variables].persist()
                        ds_mdl = xr.open_dataset(refrcst_full, engine='netcdf4')
                        da_mdl = ds_mdl[variable].persist()  


                # Pred (current year for one month and 215 days)
                ds_pred = xr.open_dataset(raw_full)
                ds_pred = xr.open_mfdataset(
                    raw_full,
                    chunks={
                        "time": len(ds_pred.time),
                        "ens": len(ds_pred.ens),
                        "lat": 'auto',
                        "lon": 'auto',
                    },
                    parallel=True,
                    engine="netcdf4",
                )
                da_pred = ds_pred[variable].persist()

                if args.crossval == True:
                    da_mdl = da_mdl.sel(time=~da_pred.time)
                    da_obs = da_obs.sel(time=~da_pred.time)

                da_temp = xr.full_like(da_pred, np.nan).persist()


                logger.info(f"Starting BC-routine for year {year}, month {month} and variable {variable}")

                # Extract forecasted dates (ignore year)
                forecast_dates = da_pred["time"].values

                # Extract available dates from the reforecast dataset
                reforecast_dates = da_mdl["time"].values    

                # Extract available dates from the reforecast dataset
                reference_dates = da_obs["time"].values   

                window = domain_config['bc_params']['window']
                
                nts = args.Horizon or len(forecast_dates)

                # Loop over each forecasted day
                for forecast_date in forecast_dates[:nts]:
                    
                    logger.info(f"Correcting time-step {forecast_date}")

                    # Define window around the forecasted day
                    start_window = forecast_date - pd.Timedelta(days=window)
                    end_window = forecast_date + pd.Timedelta(days=window)

                    da_obs_sub = da_obs.sel(time=[t for t in da_obs.time.values if within_window(t, start_window, end_window)])
                    #da_obs_sub.to_netcdf('Ref_sub.nc')

                    da_mdl_sub = da_mdl.sel(time=[t for t in da_mdl.time.values if within_window(t, start_window, end_window)])

                    da_mdl_sub = da_mdl_sub.stack(
                        ens_time=("ens", "time"), create_index=True
                    )
                    da_mdl_sub = da_mdl_sub.drop_vars("time")

                    # Select current timestep in prediction data
                    da_pred_sub = da_pred.sel(time=forecast_date)

                    da_temp.loc[forecast_date] = xr.apply_ufunc(
                       bc_module,
                       da_pred_sub,
                       da_obs_sub,
                       da_mdl_sub,
                       kwargs={
                           "bc_params": domain_config["bc_params"],
                           "precip": variable_config[variable]["isprecip"],
                       },
                       input_core_dims=[["ens"], ["time"], ["ens_time"]],
                       output_core_dims=[["ens"]],
                       vectorize=True,
                       dask="parallelized",
                       output_dtypes=[np.float64],
                    )

                # Change the datatype from "object" to "float64" --> Can we somehow get around this???
                da_temp = da_temp.astype("float64")

                # Fill this variable with some data...
                ds[variable].values = da_temp.transpose(
                    "time", "ens", "lat", "lon"
                ).values

                # ...and save everything to disk..
                ds.to_netcdf(
                    pp_full,
                    mode = "w",
                    engine = "netcdf4",
                    encoding = {
                variable: encoding[variable], 
                'ens': encoding['ens'],
                'time': encoding['time'],
                'lat': encoding['lat'],
                'lon': encoding['lon']
                },
                )

    #if client:
    #    client.shutdown()

    #if cluster is not None:
    #    cluster.close()

if __name__ == "__main__":
    main()