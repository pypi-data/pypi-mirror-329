# import packages
import argparse
import json
import logging
import os
import sys
from os.path import exists
import shutil
import dask
import numpy as np
import xarray as xr
from dask.diagnostics import ProgressBar
from dask.distributed import Client
from rechunker import rechunk

# import dir_fnme_v2 as dir_fnme
from modules import helper_modules
from modules import regional_processing_modules
from modules import cluster_modules
from modules.logger_setup import setup_logger

# Initialize logger
logger = setup_logger(log_name="process_regional_forecasts", log_level="INFO")

def get_clas():
    parser = argparse.ArgumentParser(
        description="Creation of a new domain for BCSD",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-d", "--domain", action="store", type=str, help="Domain", required=True
    )
    parser.add_argument(
        "-m",
        "--mode",
        action="store",
        type=str,
        help="Selected mode for setup",
        required=True,
    )

    parser.add_argument(
        "-Y",
        "--Years",
        action="store",
        type=str,
        help="Years for which the processing should be executed",
        required=True,
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
        "-v",
        "--variables",
        action="store",
        type=str,
        help="Variable",
        required=False,
    )
    
    parser.add_argument(
        "-s",
        "--structure",
        action="store",
        type=str,
        help="Structure of the forecasts",
        required=False,
        default='multi-file'
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
    
    parser.add_argument("--input_file", type=str, help="Name of the input file", required=False)
    parser.add_argument("--output_file", type=str, help="Name of the output file", required=False)
    parser.add_argument("--grid_file", type=str, help="Name of the output file", required=False)


    return parser.parse_args()


def process_forecast(mode, func, args, domain_config, variable_config, reg_dir_dict, grid_file):
    """
    Generalized function to iterate over variables, years, and months 
    while applying a specific processing function.

    Parameters:
    - mode (str): The processing mode (e.g., "truncate_forecasts", "remap_forecasts").
    - func (callable): The function to execute for each combination.
    - args (Namespace): Parsed command-line arguments.
    - domain_config (dict): Domain-specific configuration.
    - variable_config (dict): Variable-specific configuration.
    - reg_dir_dict (dict): Directory paths.
    - grid_file (str): Grid file path.
    """

    results = []

    for variable in variable_config:
        for year in helper_modules.decode_processing_years(args.Years):
            for month in (
                helper_modules.decode_processing_months(args.Months)
                if args.Months
                else range(1, 13)
            ):
                # Prepare arguments dynamically
                func_args = [
                    domain_config,
                    variable_config,
                    reg_dir_dict,
                    year,
                    month,
                    variable,
                ]

                if mode == "truncate_forecasts":
                    func_args.append(args.input_file if args.input_file else None)
                    func_args.append(args.output_file)

                elif mode == "remap_forecasts":
                    func_args.append(grid_file)
                    
                    
                print('oas')

                results.append(func(*func_args))

    # Execute with Dask for parallelization
    try:
        with ProgressBar():
            dask.compute(results)
        logging.info(f"{mode}: Successful execution")
    except Exception as err:
        logging.error(f"{mode}: Something went wrong: {err}")





if __name__ == "__main__":
    
    logging.info("\n".join([
        "[run_bcsd] ----------------------------------",
        "[run_bcsd]       Pycast S2S Preprocessing    ",
        "[run_bcsd] ----------------------------------",
        "[run_bcsd]             Version 0.1           ",
        "[run_bcsd] ----------------------------------",
    ]))
    
    # Read the command line arguments
    args = get_clas()

    # Create a new logger file (or append to an existing file)
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

    try:
        domain_config = domain_config[args.domain]
    except:
        logging.error(f"Init: no configuration for domain {args.domain}")
        sys.exit()

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

    if args.input_file and args.output_file and args.grid_file:
        reg_dir_dict = {}
        glob_dir_dict = {}
        grid_file = regional_processing_modules.create_grd_file(domain_config, args.grid_file)
    else:
        reg_dir_dict, glob_dir_dict = helper_modules.set_and_make_dirs(domain_config)

        # get filename of grid-File
        grid_file = f"{reg_dir_dict['static_dir']}/domain_grid.txt"

        grid_file = regional_processing_modules.create_grd_file(domain_config, grid_file)

    process_years = helper_modules.decode_processing_years(args.Years)
    print(process_years)
    if args.Months is not None:
        process_months = helper_modules.decode_processing_months(args.Months)

    # Get some ressourcers
    if args.partition is not None:
        client, cluster = cluster_modules.getCluster(
            args.partition, args.nodes, args.ntasks
        )

        client.get_versions(check=True)
        client.amm.start()

        print(f"[run_bcsd] Dask dashboard available at {client.dashboard_link}")
    
    
    ###### PROCESSING FUNCTIONS START HERE #############
    if args.mode == "truncate_forecasts":

        process_forecast(
            "truncate_forecasts",
            regional_processing_modules.truncate_forecasts,
            args,
            domain_config,
            variable_config,
            reg_dir_dict,
            grid_file,
        )

    elif args.mode == "remap_forecasts":

        results = []

        for variable in variable_config:

            for year in process_years:

                for month in process_months:
                    
                    # Prepare function call with optional arguments only when necessary
                    remap_args = [
                        domain_config,
                        reg_dir_dict,
                        year,
                        month,
                        grid_file,
                        variable,
                    ]

                    results.append(
                        regional_processing_modules.remap_forecasts(
                            domain_config,
                            reg_dir_dict,
                            year,
                            month,
                            grid_file,
                            variable,
                        )
                    )

        try:
            with ProgressBar():
                dask.compute(results)
            logging.info("Remap forecasts: successful")

        except:
            logging.error("Remap forecasts: Something went wrong")

    #

    # Concat SEAS5-Forecast on a daily Basis for calibration period or other desired period
    elif args.mode == "concat_forecasts_daily":
        syr_calib = domain_config["syr_calib"]
        eyr_calib = domain_config["eyr_calib"]
        
        # Loop over variables, years, and months and save filenames of all selected forecasts in a list
        for month in process_months:

            for variable in variable_config:
                flenms = []
                for year in range(syr_calib, eyr_calib+1):

                    if year <= 2016:
                        file_in = f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{year}{month:02d}_{domain_config['target_resolution']}.nc"
                    else:
                        file_in = f"{domain_config['variable_mapping'][variable]['forecasts']['product_prefix']}_{variable}_{year}{month:02d}_{domain_config['target_resolution']}.nc"
                        
                    full_in = f"{reg_dir_dict['raw_forecasts_target_resolution_dir']}/{file_in}"

                    flenms.append(full_in)


                # Now, let's open all files and concat along the time-dimensions
                ds = xr.open_mfdataset(
                    flenms,
                    parallel=True,
                    chunks={"time": 5, "ens": 25, "lat": "auto", "lon": "auto"},
                    engine="netcdf4",
                    autoclose=True,
                )

                # We need this step, because otherwise the chunks are not equally distributed....
                ds = ds.chunk({"time": 5, "ens": 25, "lat": "auto", "lon": "auto"})


                if process_years[0] == syr_calib and process_years[-1] == eyr_calib:
                    zarr_out =  f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{month:02d}_{domain_config['target_resolution']}_calib.zarr"
                else:
                    zarr_out =  f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{process_years[0]}_{process_years[-1]}_{month:02d}_{domain_config['target_resolution']}.zarr"

                full_out = f"{reg_dir_dict['raw_forecasts_zarr_dir']}{zarr_out}"

                # First, let's check if a ZARR-file exists
                if exists(full_out):
                    try:
                        ds.to_zarr(full_out, mode="a", append_dim="time")
                        logging.info("Concat forecast: appending succesful")
                    except:
                        logging.error(
                            "Concat forecast: something went wrong during appending"
                        )

                else:
                    coords = {
                        "time": ds["time"].values,
                        "ens": ds["ens"].values,
                        "lat": ds["lat"].values.astype(np.float32),
                        "lon": ds["lon"].values.astype(np.float32),
                    }

                    encoding = helper_modules.set_zarr_encoding(variable_config)

                    try:
                        ds.to_zarr(full_out, encoding={variable: encoding[variable]})
                        logging.info("Concat forecast: writing to new file succesful")
                    except:
                        logging.error("Concat forecast: writing to new file failed")



    elif args.mode == "rechunk_forecasts":
        for variable in variable_config:
            for month in process_months:

                if process_years[-1] < 2017:
                    zarr_in = f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{month:02d}_{domain_config['target_resolution']}_calib.zarr"
                else:
                    zarr_in = f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{process_years[0]}_{process_years[-1]}_{month:02d}_{domain_config['target_resolution']}.zarr"

                full_in = f"{reg_dir_dict['raw_forecasts_zarr_dir']}{zarr_in}"

                if process_years[-1] < 2017:
                    zarr_out = f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{month:02d}_{domain_config['target_resolution']}_calib_linechunks.zarr"
                else:
                    zarr_out = f"{domain_config['variable_mapping'][variable]['reforecasts']['product_prefix']}_{variable}_{month:02d}_{domain_config['target_resolution']}_linechunks.zarr"

                full_out = f"{reg_dir_dict['raw_forecasts_zarr_dir']}{zarr_out}"

                intermed = f"{reg_dir_dict['raw_forecasts_zarr_dir']}intermed.zarr"

                # Delete the directory of the intermediate files
                if exists(intermed):
                    shutil.rmtree(intermed)

                # This needs to be changed as we might want to add more data to the ZARR stores
                if exists(full_out):
                    shutil.rmtree(full_out)

                ds = xr.open_zarr(
                    full_in, chunks={"time": 5, "ens": 25, "lat": "auto", "lon": "auto"}
                )

                encoding = helper_modules.set_zarr_encoding(variable_config)
                
                ds = ds.chunk({"time": len(ds.time), "ens": len(ds.ens), "lat": "auto", "lon": "auto"})
                
                ds.to_zarr(full_out, encoding={variable: encoding[variable], 'lat': encoding['lat'], 'lon': encoding['lon'], 'time': encoding['time']})
                


    elif args.mode == "truncate_reference":

        for variable in variable_config:
            
            results = []
            
            for year in process_years:

                results.append(
                    regional_processing_modules.truncate_reference(
                        domain_config,
                        variable_config,
                        reg_dir_dict,
                        year,
                        variable,
                    )
                )

            try:
                dask.compute(results)
                logging.info("Truncate reference: successful")
            except Exception as err:
                logging.warning(f"Truncate reference: Something went wrong: {err}")

    # calculate t2plus and t2minus
    elif args.mode == "calc_t2plus_minus":
        # variable config only for t2plus and t2minus
        # Read the variable configuration from the respective JSON
        with open("conf/variable_config.json", "r") as j:
            variable_config = json.loads(j.read())

        variable_config_t2plus_minus = {
            key: value
            for key, value in variable_config.items()
            if key in ["t2plus", "t2minus"]
        }

        for year in process_years:
            fnme_lst = []
            # load t2m
            file_t2m = f"{domain_config['reference_history']['prefix']}_t2m_{year}.nc"
            full_t2m = f"{reg_dir_dict['reference_initial_resolution_dir']}/{file_t2m}"
            fnme_lst.append(full_t2m)
            # t2max
            file_t2max = f"{domain_config['reference_history']['prefix']}_t2max_{year}.nc"
            full_t2max = f"{reg_dir_dict['reference_initial_resolution_dir']}/{file_t2max}"
            fnme_lst.append(full_t2max)
            # t2min
            file_t2min = f"{domain_config['reference_history']['prefix']}_t2min_{year}.nc"
            full_t2min = f"{reg_dir_dict['reference_initial_resolution_dir']}/{file_t2min}"
            fnme_lst.append(full_t2min)

            # Open all together
            ds = xr.open_mfdataset(
                fnme_lst,
                parallel=True,
                chunks={"time": 50},
                engine="netcdf4",
                autoclose=True,
            )

            try:
                # drop time_bounds
                ds = ds.drop_vars("time_bnds")
            except:
                print("no bnds available")

            # Calculate t2plus and t2minus
            ds["t2plus"] = ds.t2max - ds.t2m
            ds["t2minus"] = ds.t2m - ds.t2min

            # t2max
            file_t2plus = f"{domain_config['reference_history']['prefix']}_t2plus_{year}.nc"
            full_t2plus= f"{reg_dir_dict['reference_initial_resolution_dir']}/{file_t2plus}"

            # t2min
            file_t2minus = f"{domain_config['reference_history']['prefix']}_t2minus_{year}.nc"
            full_t2minus = f"{reg_dir_dict['reference_initial_resolution_dir']}/{file_t2minus}"

            coords = {
                "time": ds["time"].values,
                "lat": ds["lat"].values.astype(np.float32),
                "lon": ds["lon"].values.astype(np.float32),
            }

            encoding = helper_modules.set_encoding(variable_config_t2plus_minus, coords)

            # Store as netcdf
            try:
                ds["t2plus"].to_netcdf(full_t2plus, encoding={"t2plus": encoding["t2plus"]})
                ds["t2minus"].to_netcdf(full_t2minus, encoding={"t2minus": encoding["t2minus"]})
            except:
                print("Calculation t2plus, t2minus: something went wrong")


    elif args.mode == "remap_reference":

        results = []

        for variable in variable_config:

            for year in process_years:

                results.append(
                    regional_processing_modules.remap_reference(
                        domain_config,
                        reg_dir_dict,
                        year,
                        grid_file,
                        variable,
                    )
                )

        try:
            with ProgressBar():
                dask.compute(results)
            logging.info("Remap forecasts: successful")
        except Exception as err:
            logging.error("Remap forecasts: Something went wrong: {err}")

   
    # Concat reference for BCSD (for calibration period) or for any desired period (daily-data)
    elif args.mode == "concat_reference_daily":
        syr_calib = domain_config["syr_calib"]
        eyr_calib = domain_config["eyr_calib"]

        # Loop over variables, years, and months and save filenames of all selected forecasts in a list
        for variable in variable_config:
            
            varname_reference = domain_config['variable_mapping'][variable]['reference']['varname']
            
            filenames = []
            
            for year in range(syr_calib, eyr_calib+1):
                
                file_in = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{year}_{domain_config['target_resolution']}.nc"
                full_in = (f"{reg_dir_dict['reference_target_resolution_dir']}/{file_in}")

                filenames.append(full_in)

            # Now, let's open all files and concat along the time-dimensions
            ds = xr.open_mfdataset(
                filenames,
                parallel=False,
                # chunks={'time': 5, 'lat': 'auto', 'lon': 'auto'},
                engine="netcdf4",
                autoclose=True,
            )

            if process_years[0] == syr_calib and process_years[-1] == eyr_calib:
                zarr_out = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{domain_config['target_resolution']}_calib.zarr"
            else:
                zarr_out = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{process_years[0]}_{process_years[-1]}_{domain_config['target_resolution']}.zarr"

            full_out = f"{reg_dir_dict['reference_zarr_dir']}{zarr_out}"

            ds = ds.chunk({"time": 50})

            # First, let's check if a ZARR-file exists
            if exists(full_out):
                try:
                    ds.to_zarr(full_out, mode="a", append_dim="time")
                    logging.info("Concat forecast: appending succesful")
                except:
                    logging.error("Concat forecast: something went wrong during appending")

            else:
                coords = {
                    "time": ds["time"].values,
                    "lat": ds["lat"].values.astype(np.float32),
                    "lon": ds["lon"].values.astype(np.float32),
                }

                encoding = helper_modules.set_zarr_encoding(variable_config)
                try:
                    ds.to_zarr(full_out, encoding={varname_reference: encoding[variable]})
                    logging.info("Concat forecast: writing to new file succesful")
                except:
                    logging.error("Concat forecast: writing to new file failed")


    # Rechunk reference for calibration period or for other periods (other periods are not tested yet)
    elif args.mode == "rechunk_reference":
        syr_calib = domain_config["syr_calib"]
        eyr_calib = domain_config["eyr_calib"]
        for variable in variable_config:
            # set input files
            if process_years[0] == syr_calib and process_years[-1] == eyr_calib:
                zarr_in = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{domain_config['target_resolution']}_calib.zarr"
            else:
                zarr_in = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{process_years[0]}_{process_years[-1]}_{domain_config['target_resolution']}.zarr"

            full_in = f"{reg_dir_dict['reference_zarr_dir']}{zarr_in}"

            # set output files
            if process_years[0] == syr_calib and process_years[-1] == eyr_calib:
                zarr_out = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{domain_config['target_resolution']}_calib_linechunks.zarr"
            else:
                zarr_out = f"{domain_config['variable_mapping'][variable]['reference']['product_prefix']}_{variable}_{process_years[0]}_{process_years[-1]}_{domain_config['target_resolution']}_linechunks.zarr"

            full_out = f"{reg_dir_dict['reference_zarr_dir']}{zarr_out}"

            intermed = f"{reg_dir_dict['reference_zarr_dir']}intermed.zarr"

            # Delete the directory of the intermediate files
            if exists(intermed):
                shutil.rmtree(intermed)

            # This needs to be changed as we might want to add more data to the ZARR stores
            if exists(full_out):
                shutil.rmtree(full_out)

            ds = xr.open_zarr(full_in, chunks={"time": 50, "lat": "auto", "lon": "auto"})

            encoding = helper_modules.set_zarr_encoding(variable_config)

            rechunked = rechunk(
                ds,
                target_chunks={"time": len(ds.time), "lat": 1, "lon": 1},
                target_store=full_out,
                max_mem="2000MB",
                temp_store=intermed,
                target_options=encoding,
            )

            with ProgressBar():
                rechunked.execute()



##
## PROCESSING OF MONTHLY STUFF
##



    # Concat SEAS5-Forecast on a daily Basis for calibration period or other desired period
    elif args.mode == "concat_forecasts_monthly":
        syr_calib = domain_config["syr_calib"]
        eyr_calib = domain_config["eyr_calib"]


        # Loop over variables, years, and months and save filenames of all selected forecasts in a list
        for month in process_months:
            # create list of month, which are included in SEAS5
            month_end = month + 8
            if month_end < 14:
                month_range = np.arange(month, month_end)
            else:
                month_range_1 = np.arange(month, 13)
                month_range_2 = np.arange(1, month_end - 12)
                month_range = np.concatenate((month_range_1, month_range_2), axis=0)
            # Store it as a list
            month_range = list(month_range)
            print(month_range)

            for variable in variable_config:
                flenms = []
                for year in process_years:
                    fle_in = f"{domain_config['raw_forecasts']['prefix']}_{variable}_{year}{month:02d}_{domain_config['target_resolution']}.nc"
                    full_in = f"{reg_dir_dict['raw_forecasts_target_resolution_dir']}/{fle_in}"

                    flenms.append(full_in)

                # Now, let's open all files and concat along the time-dimensions
                ds = xr.open_mfdataset(
                    flenms,
                    parallel=True,
                    chunks={"time": 5, "ens": 25, "lat": "auto", "lon": "auto"},
                    engine="netcdf4",
                    autoclose=True,
                )

                # Take monthly mean for each year
                ds_mon = ds.resample(time="1MS").mean()
                # Only select the months which are needed, because resample add nan-values for other months, which we are not interested in
                ds_mon = ds_mon.sel(time=ds_mon.time.dt.month.isin(month_range))

                # We need this step, because otherwise the chunks are not equally distributed....
                ds_mon = ds_mon.chunk({"time": 5, "ens": 25, "lat": "auto", "lon": "auto"})


                if process_years[0] == syr_calib and process_years[-1] == eyr_calib:
                    zarr_out = f"{domain_config['raw_forecasts']['prefix']}_mon_{variable}_{month:02d}_{domain_config['target_resolution']}_calib.zarr"
                else:
                    zarr_out = f"{domain_config['raw_forecasts']['prefix']}_mon_{variable}_{process_years[0]}_{process_years[-1]}_{month:02d}_{domain_config['target_resolution']}.zarr"

                full_out = f"{reg_dir_dict['seas_forecast_mon_zarr_dir']}{zarr_out}"

                # First, let's check if a ZARR-file exists
                if exists(full_out):
                    try:

                        ds_mon.to_zarr(full_out, mode="a", append_dim="time")
                        logging.info("Concat forecast: appending succesful")
                    except:

                        logging.error(
                            "Concat forecast: something went wrong during appending"
                        )

                else:
                    coords = {
                        "time": ds["time"].values,
                        "ens": ds["ens"].values,
                        "lat": ds["lat"].values.astype(np.float32),
                        "lon": ds["lon"].values.astype(np.float32),
                    }

                    encoding = helper_modules.set_zarr_encoding(variable_config)

                    try:

                        ds_mon.to_zarr(full_out, encoding={variable: encoding[variable]})
                        logging.info("Concat forecast: writing to new file succesful")
                    except:

                        logging.error("Concat forecast: writing to new file failed")
                        
                        
    # Concat reference for BCSD (for calibration period) or for any desired period (monthly data))
    elif args.mode == "concat_reference_monthly":
        syr_calib = domain_config["syr_calib"]
        eyr_calib = domain_config["eyr_calib"]


        # Loop over variables, years, and months and save filenames of all selected forecasts in a list
        for variable in variable_config:
            filenames = []
            for year in process_years:
                file_out = f"{domain_config['reference_history']['prefix']}_{variable}_{year}_{domain_config['target_resolution']}.nc"
                full_out = (
                    f"{reg_dir_dict['reference_target_resolution_dir']}/{file_out}"
                )

                filenames.append(full_out)

            # Now, let's open all files and concat along the time-dimensions
            ds = xr.open_mfdataset(
                filenames,
                parallel=True,
                # chunks={'time': 5, 'lat': 'auto', 'lon': 'auto'},
                engine="netcdf4",
                autoclose=True,
            )
            ds_mon = ds.resample(time="1MS").mean()

            if process_years[0] == syr_calib and process_years[-1] == eyr_calib:
                zarr_out = f"{domain_config['reference_history']['prefix']}_mon_{variable}_{domain_config['target_resolution']}_calib.zarr"
            else:
                zarr_out = f"{domain_config['reference_history']['prefix']}_mon_{variable}_{process_years[0]}_{process_years[-1]}_{domain_config['target_resolution']}.zarr"

            full_out = f"{reg_dir_dict['ref_forecast_mon_zarr_dir']}{zarr_out}"

            ds = ds.chunk({"time": 50})

            # First, let's check if a ZARR-file exists
            if exists(full_out):
                try:
                    ds_mon.to_zarr(full_out, mode="a", append_dim="time")
                    logging.info("Concat forecast: appending succesful")
                except:
                    logging.error("Concat forecast: something went wrong during appending")

            else:
                coords = {
                    "time": ds["time"].values,
                    "lat": ds["lat"].values.astype(np.float32),
                    "lon": ds["lon"].values.astype(np.float32),
                }

                encoding = helper_modules.set_zarr_encoding(variable_config)
                try:
                    ds_mon.to_zarr(full_out, encoding={variable: encoding[variable]})
                    logging.info("Concat forecast: writing to new file succesful")
                except:
                    logging.error("Concat forecast: writing to new file failed")

