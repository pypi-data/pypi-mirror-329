<!--
SPDX-FileCopyrightText: 2022 - Karlsruhe Institute of Technology - KIT

SPDX-License-Identifier: GPL-3.0-or-later
-->

<a href="https://www.imk-ifu.kit.edu">
    <img src="https://intranet.imk-ifu.kit.edu/wiki/lib/exe/fetch.php?media=formulare:logos:kitlogo_4c_deutsch_ohnehintergrund.png" width="180"/>
</a>

<a href="https://www.imk-ifu.kit.edu">
    <img src="https://intranet.imk-ifu.kit.edu/wiki/lib/exe/fetch.php?media=formulare:logos:logo_campusalpin_en_rgb.jpg" align="right" width="200"/>
</a>

# IMK-IFU Forecast processing toolbox
This python package contains tools for an operational processing of forecasts. In the end, PyCast should cover the whole processing chain of seasonal forecasts, ranging from the truncation of global forecasts to a specific study domain, the re-structuring of ensemble forecasts to a pre-defined format, the bias-correction using a quantile-mapping approach as well as the forecast evaluation and the transformation of ensemble forecasts into more user-oriented products like categorical forecasts or climate indicators.

## Getting Started...
In this tutorial, we will guide you through through the processing of a seasonal forecast, including the truncation to the study domain, the remapping to a higher resolved grid and, last but not least, the quantile-mapping based bias correcation towards some chosen reference data. For this, we are using seasonal forecasts from ECMWF as well as reference data from the ERA5-Land model. As study domain, we've chosen a small part of the Ethiopian Highlands, where a large part of the Nile-water is coming from. But this can and should be adapted to your needs!

### Step 1: Get your machine ready...
- Get some tool for visualizing NetCDF data (Panoply, ncview, Python/Xarray, etc.)
- Clone the Pycast-Repository: 
    `git clone https://codebase.helmholtz.cloud/kit-seasonal-forecast-task-force/pycast-s2s.git`
- Navigate into cloned repository:
	`cd pycast-s2s`
- Switch to the workshop branch:
    `git checkout workshop`
- To start a Bash shell session type:
	`bash`
- Create a virtual environment to hold all the libraries and dependencies
    `python -m venv .venv`
- Activate the virtual environment
  - on Windows: `.venv/Scripts/activate`
  - On Mac/Linux: `source .venv/bin/activate`
- Install the required libraries
    `pip install -r requirements.txt`
- Add virtual environment to Jupyter
    `python -m ipykernel install --user --name=pycast_workshop`

### Step 2: Download some demonstrator data
- Go to https://thredds.imk-ifu.kit.edu/thredds/catalog/projects/s2s/pycast_workshop/catalog.html (this is where you get the data for the workshop from)
- Download the following files:
  - `SEAS5_t2m_202501.nc` --> First two ensemble members of the forecast from January 2025, truncated to a larger domain across Ethiopia and Sudan.
  - `SEAS5_t2m_Jan_2000_to_2016.nc` --> First two ensemble members of the re-forecasts during the period 2000 to 2016.
  - `ERA5_Land_t2m_2000_to_2016.nc` --> Reference data during the period 2000 to 2016.
- Hint for Windows: download the files via HTTPServer 
- Hint for Linux/maxOS: download the files using the link of HTTPServer:
	`curl -O "https://thredds.example.com/path/to/dataset.nc"`
	or `wget "https://thredds.example.com/path/to/dataset.nc"` 
- Put all the files into a folder thats easy to remember (preferabbly a data-folder in the pycast-s2s folder)
	- Hint for creating a new directory: `mkdir data`
From these files, the reforecasts and reference data were already truncated to the study domain so we only have to process the actual forecast data. 

### Step 3: Do the pre-processing of the forecasts
For this demonstrator, we're assuming that the files are located in the `/data`-directory in your main pycast-folder and that you have navigated into src-folder with `cd src`.

#### Truncation to a study domain
Go to the pycast-s2s/src-folder and enter the following command:
 `python3 process_regional_forecasts.py -d demonstrator -m truncate_forecasts -v t2m --input_file ../data/SEAS5_t2m_202501.nc --output_file ../data/SEAS5_t2m_202501_truncated.nc --grid_file ../data/grid.txt`
This will truncate the raw forecasts to our study domain. We will now go very briefly through the function call:
- `-d`: Domain name that is defined in the `conf/domain_config.json` file. For this tutorial, we have defined a small domain with the name demonstrator. 
- `-m`: Select a mode, can be set to `truncate_forecasts` or `remap_forecasts`; the function supports other modes as well, but we will only use these two here
- `-v`: Select a variable name; note that if we run our preprocessor with user-defined files, this variable must be consistent across all input data; if we choose to run the automatic mode (where all filenames are defined automatically), the variable names of the different input data as well as their mapping are defined in the config file
- `-input_file`: Select the name of the raw forecasts, that should be truncated to the study domain
- `-output_file`: Select the name of the truncated file

#### Remap forecasts to the final grid
Go to the pycast-s2s/src-folder and enter the following command:
 `python3 process_regional_forecasts.py -d demonstrator -m remap_forecasts -v t2m --input_file ../data/SEAS5_t2m_202501_truncated.nc --output_file ../data/SEAS5_t2m_202501_remapped.nc --grid_file ../data/grid.txt`
This will remap the raw forecasts to the target resolution, that is also defined in our `conf/domain_config.json` file. 
- `--grid_file`: Name of the grid definition file, that contains the corners of the bounding box as well as the resolution of the target grid.

#### Run the bias correction
 `python3 run_bcsd.py -d demonstrator -v t2m -s 4D -H 5 --raw_forecast ../data/SEAS5_t2m_202501_remapped.nc  --bc_forecast ../data/SEAS5_t2m_202501_tabn_bcsd.nc --reforecasts ../data/SEAS5_t2m_Jan_2000_to_2016.nc --reference ../data/ERA5_Land_t2m_2000_to_2016.nc`
This command finally starts the bias-correction and runs across all ensemble member and forecast time steps of the provided forecasts. 
- `-s`: Structure of the forecasts; this can be set to `4D` [time X ens X lat X lon] or `5D` [year X lead_time X ens X lat X lon] --> normally, whe should use the `4D`-structure. But for forecasts that have a horizon of more than 1 year, we might have to use the `5D`-structure
- `-H`: Forecast horizion that should be corrected. IN this example, we only want to correct the first 5 time-steps so that we do not have to wait too long. 
- `--raw_forecast`: Filename of the remapped forecasts
- `--bc_forecast`: Filename of the bias-corrected forecasts (i.e., the output)
- `--reforecasts`: Filename of the reforecasts, that are used for calculating the climatology
- `--reference`: Filename of the reference data

#### Explore the results and change some parameters
Now, you should be able to see your bias-corrected file in the data-directory. Please start Jupyter and explore the data. If you want, you can also go to the conf-directory and change the parameters of the demonstrator domain. In particular, you can change the number of quantiles, which will greatly impact the peformance or the size of the time-window that is used for calculating the statistics.