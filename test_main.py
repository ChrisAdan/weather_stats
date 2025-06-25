import pytest
import pandas as pd
from main import validate_schema, COLUMNS

def test_validate_schema_valid():
    df = pd.DataFrame(columns=COLUMNS + ['test_other_col'])
    assert validate_schema(df) == True

def test_validate_schema_invalid():
    df = pd.DataFrame(columns=['DATE', 'NAME']) # missing required columns
    assert validate_schema(df) == False