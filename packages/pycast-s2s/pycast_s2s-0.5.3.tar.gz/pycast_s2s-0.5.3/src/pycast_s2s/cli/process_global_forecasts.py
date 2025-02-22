# import packages
import argparse
import json
import logging
import os
import sys

from tqdm import tqdm

from itertools import product


import dask
from dask.distributed import progress
from genericpath import exists

import datetime

#sys.path.append(os.path.abspath('..'))
#sys.path.append(os.path.abspath('../src/modules'))

from modules import global_processing_modules
from modules import helper_modules
from modules import cluster_modules


def get_clas():

    parser = argparse.ArgumentParser(
        description="Creation of a new domain for BCSD",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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

    return parser.parse_args()


def setup_logger():
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    
    os.makedirs(os.path.dirname(f"logs/global_processing_{timestamp}.log"), exist_ok=True)

    logging.basicConfig(
        filename=f"logs/global_processing_{timestamp}.log",
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    # encoding='utf-8'

def main():
    print("""
    [global_processing] ----------------------------------
    [global_processing]    Pycast S2S Global Processing   
    [global_processing] ----------------------------------
    [global_processing]             Version 0.1           
    [global_processing] ----------------------------------
    """)

    # Read the command line arguments
    args = get_clas()

    # Create a new logger file (or append to an existing file)
    setup_logger()

    with open("conf/global_config.json", "r") as j:
        global_config = json.loads(j.read())
        
    # Read the global configuration from the respective JSON --> Add this as further input parameter
    with open("conf/attribute_config.json", "r") as j:
        attribute_config = json.loads(j.read())
        
    # Read the variable configuration from the respective JSON
    with open("conf/variable_config.json", "r") as j:
        variable_config = json.loads(j.read())
        
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
            if key in global_config["variables"]
        }
        

    ########################################################

    process_years = helper_modules.decode_processing_years(args.Years)

    if args.Months is not None:
        process_months = helper_modules.decode_processing_months(args.Months)

    # Get some ressourcers
    client, cluster = cluster_modules.getCluster(args.partition, args.nodes, args.ntasks)
    print(f"[global_processing] Dask dashboard available at {client.dashboard_link}")

    # Get the total number of iterations for showing a nice progress bar
    nyears = len(process_years)
    nmonths = len(process_months)
    nvars = len(variable_config)
    total_iterations = nyears * nmonths * nvars

    
    if args.mode == "1":
        
        progress_bar = tqdm(total=total_iterations, desc="Gauss to regular")
        results = []

        #if not global_config["raw_forecasts"]["merged_variables"]:
        #    for year, month, var in product(process_years, process_months, global_config["variables"]):
        #        
        #        flenme_grb = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_{var}_{year}{month:02d}.grb"
        #        flenme_nc = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_{var}_{year}{month:02d}.nc"
        #        
        #        results.append(
        #            global_processing_modules.gauss_to_regular(global_config, year, month, var)
        #        )
        #        progress_bar.update(1)
                
        #else:
        for year, month in product(process_years, process_months):
            flenme_grb = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_24h_{year}{month:02d}.grb"
            flenme_nc = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_24h_{year}{month:02d}.nc"
            
            results.append(global_processing_modules.gauss_to_regular(flenme_grb, flenme_nc))
                
            
        dask.compute(results)
        #logging.info(
        #    f"[global_processing] Gauss to regular: Coordination transformation for {year} {month} successful"
        #)

        # Block for renaming all variables per file
        #progress_bar_rename = tqdm(total=total_iterations, desc="Renaming variables")#

       # for year in process_years:

        #    for month in process_months:

        #        for var in global_config["variables"]:

        #            global_processing_modules.rename_variable(global_config, year, month, var)

        #            progress_bar_rename.update(1)

        #logging.info(
        #        f"[global_processing] Renaming variables: Renaming successful for {year} {month}"
        #)

    elif args.mode == "2":
        # Here goes the block that re-structures the forecasts. 
        
        # Here this line should be adapted to True/False depending, but for now solved with mode description 
        # if global_config["raw_forecasts"]["merged_variables"] == False:
            
        # Update total iterations for progress_bar without variable dimension    
        total_iterations = nyears * nmonths

        progress_bar = tqdm(total=total_iterations, desc="Gauss to regular")

        results = []

        for year in process_years:

            for month in process_months:
                
                results.append(
                        global_processing_modules.gauss_to_regular(global_config=global_config, year=year, month=month, variable=None, mode=args.mode)
                        )
                progress_bar.update(1)
                
        dask.compute(results)
        logging.info(
                f"[global_processing] Gauss to regular: Coordination transformation for {year} {month} successful"
                )
        
    elif args.mode == "unpack_forecasts":
        
        # At that stage, we only consider the forecasts where the raw downloads contain only a single variabe
        progress_bar = tqdm(total=total_iterations, desc="Unpack forecasts")
        
        results = []
        
        for year in process_years:
            
            for month in process_months:
                
                for var in variable_config:
                    
                    filename_in  = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_{var}_{year}{month:02d}.grb"
                    filename_out = f"{global_config['raw_directory']}/{year}/{month:02d}/{global_config['raw_forecasts']['prefix']}_daily_{var}_{year}{month:02d}.nc"
                    
                    global_processing_modules.unpack_forecasts(
                            variable_config=variable_config,
                            attribute_config = attribute_config,
                            filename_in = filename_in,
                            filename_out = filename_out,
                    )
                    
                    #results.append(
                    #    global_processing_modules.unpack_forecasts(
                    #        variable_config=variable_config,
                    #        global_config = global_config,
                    #        filename_in = filename_in,
                    #        filename_out = filename_out,
                    #    )
                    #)
                    
                    #progress_bar.update(1)
        #progress(results)    
        #dask.compute(results)
        
        


if __name__ == "__main__":
    main()