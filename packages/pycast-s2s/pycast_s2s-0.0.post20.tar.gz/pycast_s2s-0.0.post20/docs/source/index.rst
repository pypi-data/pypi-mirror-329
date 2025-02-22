.. PyCast S2S documentation master file, created by
   sphinx-quickstart on Sat Nov 18 23:16:39 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyCast S2S's documentation!
======================================
PyCast S2S provides a suite of tools for processing and post-processing regional climate forecast data.  It facilitates tasks such as:

* **Data Preparation:** Truncating and remapping forecast and reference data to specific domains and grids.
* **Bias Correction:** Applying the Bias Correction Spatial Disaggregation (BCSD) method to improve forecast accuracy.
* **Aggregation and Analysis:**  Calculating climatologies, monthly statistics, and other derived variables.
* **Parallel Processing:** Leveraging Dask for efficient computation on large datasets.
* **Flexible Configuration:**  Utilizing JSON configuration files for easy customization of processing parameters.

This framework is designed to be modular and extensible, allowing users to adapt it to their specific needs.  It is built upon popular Python libraries like Xarray, Dask, and others, ensuring interoperability with existing scientific workflows.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

Process_regional_forecasts.py - The tool for setting up your data
-----------------------------------------------------------------
.. automodule:: process_regional_forecasts
   :members:
   :undoc-members:   
   :show-inheritance:

Run_bcsd - The main file of PyCast S2S
--------------------------------------
.. automodule:: run_bcsd
   :members:
   :undoc-members:   
   :show-inheritance:

Regional processing modules - Helper files for the regional proccesing
---------------------------------------------------------------------
.. automodule:: modules.regional_processing_modules
   :members:
   :undoc-members:
   :show-inheritance:



The helper_modules - General helper tools for PyCast
---------------------------------------------------
.. automodule:: modules.helper_modules
   :members:
   :undoc-members:
   :show-inheritance:

The cluster_modules - Tools for setting up your cluster environment
-------------------------------------------------------------------
.. automodule:: modules.cluster_modules
   :members:
   :undoc-members:
   :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
