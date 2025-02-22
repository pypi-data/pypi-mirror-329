import pytest
import xarray as xr
from unittest.mock import patch, MagicMock
import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the src directory to the Python module search path
sys.path.append(os.path.join(parent_dir, "src"))

from modules.global_processing_modules import preprocess_rename, gauss_to_regular
from modules.helper_modules import run_cmd



# Assuming preprocess_rename is a function that renames variables in an xarray Dataset according to a mapping dictionary
# The function and mapping_dict need to be imported or defined in the test module

# Test cases are structured as follows:
# test_id: A unique identifier for the test case
# ds: The input xarray Dataset
# mapping_dict: A dictionary mapping original variable names to new names
# expected_vars: The expected variable names in the processed Dataset
# input_vars: The original variable names in the input Dataset

            

@pytest.mark.parametrize("test_id, ds, mapping_dict, expected_vars, input_vars", [
    # Happy path tests
    ("HP_01", xr.Dataset({"temp": ("x", [1, 2, 3])}), {"temp": "temperature"}, ["temperature"], ["temp"]),
    ("HP_02", xr.Dataset({"precip": ("x", [4, 5, 6]), "wind": ("x", [7, 8, 9])}), {"precip": "rainfall", "wind": "wind_speed"}, ["rainfall", "wind_speed"], ["precip", "wind"]),
    
    # Edge cases
    ("EC_01", xr.Dataset({"temp": ("x", [])}), {"temp": "temperature"}, ["temperature"], ["temp"]),  # Empty data variable
    ("EC_02", xr.Dataset(), {}, [], []),  # Empty Dataset
    
    # Error cases
    #("ER_01", xr.Dataset({"temp": ("x", [1, 2, 3])}), {"not_in_ds": "temperature"}, ["temperature"], ["temp"]),  # Variable to rename not in Dataset
    #("ER_02", xr.Dataset({"temp": ("x", [1, 2, 3])}), {"temp": "temp"}, ["temp"], ["temp"]),  # Renaming to the same name
])
def test_preprocess_rename(test_id, ds, mapping_dict, expected_vars, input_vars):
    # Act
    # Call the preprocess_rename function
    processed_ds = preprocess_rename(ds, mapping_dict)

    # Assert
    # Check if the dataset has been renamed correctly
    assert all(var in processed_ds.data_vars for var in expected_vars), f"Test {test_id} failed: Not all expected variables are in the dataset."
    assert all(original_var not in processed_ds.data_vars for original_var in input_vars if original_var in mapping_dict), f"Test {test_id} failed: Original variables should not be present after renaming."
