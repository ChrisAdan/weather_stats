import pytest
import pandas as pd
from main import validate_schema, COLUMNS

def test_validate_schema_valid():
    """
    Test validate_schema() with a DataFrame that includes all required columns.

    Asserts that the function returns True for valid input.
    """
    df = pd.DataFrame(columns=COLUMNS + ['test_other_col'])
    assert validate_schema(df) == True

def test_validate_schema_invalid():
    """
    Test validate_schema() with a DataFrame that is missing one or more required columns.

    Asserts that the function returns False for invalid input.
    """
    df = pd.DataFrame(columns=['DATE', 'NAME']) # missing required columns
    assert validate_schema(df) == False