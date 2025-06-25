# Analyzing Sample Weather Statistics

This repo organizes code for a classic data transformation and analytics task.

Given an input containing a large number (~50k) CSV files, the objective is to ingest, validate, standardize, and draw insights around temperature and other meteorological recordings from ~12K weather stations.

## Step 1: Ingest the inbound data

An initial strategy was to use the `tarfile` library in `main.py` to decompress the input directory. That proved time intensive, so instead it was extracted via Bash. Each file in the directory was looped and checked for conformity to the required column names to complete the exercise. Suitable files were appended and concatenated into a single output dataframe. Some brief sanitization steps were executed to drop missing or incomplete records. The output was be written to a CSV on disk and read into a Jupyter Notebook for analysis.

Pytest was used to validate the input files for appropriate schemas.

## Step 2: Clean and analyze

The raw data was read into a Jupyter Notebook. A subset of relevant columns and date ranges were selected and the rest dropped to save memory. After checking for sparsity in the raw data (particularly on station names), questions are answered regarding station temperature patterns and trends.

## Commentary

Great practice task. My first approach was to unpack the .tar.gz input directory programmatically so I could process the ~50K CSVs without decompressing myself. Decided that was too time intensive, so opted to unzip via Linux in Bash and refactor the script to cycle through input CSVs, validate the schemas, and export a unified dataframe to CSV for analysis in the Jupyter layer. The benefit of that change to approach was time saved, but introducing manual elements to a process cuts back on scalability.

If there were 100 years of data, depending on where those files are actually stored, I would consider more programmatic means of unpacking again, possibly parallelizing to reduce computation time, and minimizing actual memory on disk usage wherever possible.

I would also use a local DuckDB instead of a CSV for improved interface times and lighter RAM footprint.

Another note is that analysis in a Jupyter Notebook is great for ad hoc information, but for broader use cases such as dashboarding or automated reporting, a different approach to data modeling and a plan for storage would be important.

Thanks for reading!  
Chris Adan  
[Find me on LinkedIn](https://www.linkedin.com/in/chrisadan/)  
[Read on Medium](https://upandtothewrite.medium.com/)
