import pandas as pd
import json
from pathlib import Path

COLUMNS = ['STATION', 'DATE', 'NAME', 'TEMP']

CWD = Path(__file__).parent.resolve()
DATA_DIR = CWD / 'data'
RAW_TAR = DATA_DIR / 'ae_coding_screen_data.tar.gz'

DOC_DIR = CWD / 'doc'
MONITOR_FILE = DOC_DIR / 'ingestion_summary.json'  

def validate_schema(df: pd.DataFrame) -> bool:
    """
    Validate that the input DataFrame contains all required columns.

    Parameters:
        df (pd.DataFrame): The DataFrame to validate.

    Returns:
        bool: True if the DataFrame contains all required columns, False otherwise.
    """
    return set(COLUMNS).issubset(df.columns)

def load_input_data() -> pd.DataFrame:
    """
    Recursively load and validate CSV files from the 'data/' directory.

    Only rows from valid CSVs (those containing all required columns) are included.
    Also removes any MacOS metadata files beginning with '._'.
    An ingestion summary is written to 'doc/ingestion_summary.json'.

    Returns:
        pd.DataFrame: A concatenated DataFrame containing all valid records.
    """
    valid_files = []
    total_files = 0
    invalid_files = 0

    input_files = list(DATA_DIR.rglob('*.csv'))

    for csv in input_files:
        total_files += 1

        if csv.name.startswith('._'):
            try:
                csv.unlink()
                print(f'Deleted MacOS metadata file: {csv}')
            except Exception as e:
                print(f'Error deleting {csv}: {e}')
            continue

        try:
            curr = pd.read_csv(csv, encoding='latin1', keep_default_na=False)
            if validate_schema(curr):
                valid_files.append(curr)
            else:
                invalid_files += 1
        except Exception as e:
            print(f'Failed to read file {csv}: {e}')
            invalid_files += 1
        
        if total_files == 0:
            raise ValueError(f'No CSV files found in archive at {DATA_DIR}')
        
    print(f'Processed {total_files} files. {invalid_files} found invalid.')

    # dump monitoring statistics
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        'total_files':total_files,
        'valid_files':total_files - invalid_files,
        'invalid_files':invalid_files,
        'percent_invalid':round((invalid_files / total_files) * 100, 2)
    }
    with MONITOR_FILE.open('w') as f:
        json.dump(summary, f, indent=2)
    
    print(f'Processed {total_files} files. {invalid_files} invalid')
    print(f'Wrote ingestion summary to {MONITOR_FILE}')
    return pd.concat(valid_files, ignore_index=True)

if __name__ == '__main__':
    full_input = load_input_data()
    full_input.to_csv(DATA_DIR / 'weather_statistics.csv', index=False)
    print(f'Process Complete')
