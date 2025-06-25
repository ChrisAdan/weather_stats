import pandas as pd
import io
import json
from pathlib import Path
import chardet

COLUMNS = ['STATION', 'DATE', 'NAME', 'TEMP']

CWD = Path(__file__).parent.resolve()
DATA_DIR = CWD / 'data'
RAW_TAR = DATA_DIR / 'ae_coding_screen_data.tar.gz'

DOC_DIR = CWD / 'doc'
MONITOR_FILE = DOC_DIR / 'ingestion_summary.json'  

def validate_schema(df: pd.DataFrame) -> bool:
    return set(COLUMNS).issubset(df.columns)

def get_encoding(file) -> str:
    content = file.read(10000)
    encoding = chardet.detect(content)['encoding']
    file.seek(0)
    return encoding

def load_input_data() -> pd.DataFrame:
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


# make sure to convert F to C


if __name__ == '__main__':
    full_input = load_input_data()
    full_input.to_csv(DATA_DIR / 'weather_statistics.csv', index=False)
    print(f'Process Complete')
