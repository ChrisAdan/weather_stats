# Analyzing Sample Weather Statistics

This repo organizes code for a classic data transformation and analytics task.

Given an input containing a large number (~50k) CSV files, the objective is to ingest, validate, standardize, and draw insights around temperature and other meteorological recordings from ~12K weather stations.

## Step 1: Ingest the inbound data

Strategy will be to use the `tarfile` library in `main.py` to decompress the input directory. We will loop through each file in the directory and check for conformity to the required column names to complete the exercise. Suitable files will be appended and concatenated into a single output dataframe. Some brief sanitization steps will be executed to drop missing or incomplete records. The output will be written to a CSV on disk and read into a Jupyter Notebook for analysis.

Thanks for reading!
Chris Adan  
[Find me on LinkedIn](https://www.linkedin.com/in/chrisadan/)  
[Read on Medium](https://upandtothewrite.medium.com/)
