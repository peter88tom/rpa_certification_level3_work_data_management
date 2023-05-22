"""
Produce traffic data work items
"""
from RPA.HTTP import HTTP
import pandas as pd
from RPA.Tables import Tables
from RPA.JSON import JSON

# Traffic data API
traffic_data_api = "https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json"

# Path to Json data file after downloding from the API
traffic_json_file_path = "output/traffic.json"

# Varibles for technical names and numbers
max_rate = "5.0"
rate_key = "NumericValue"
gender_key = "Dim1"
both_genders = "BTSX"
year_key = "TimeDim"


def download_traffic_data():
    """ 
        Download the trafic data.
        https://robocorp.com/docs/courses/work-data-management/download-the-traffic-data
    """
    http = HTTP()
    http.download(url=traffic_data_api, overwrite=True,
                  target_file="output/traffic.json")


def filter_and_sort_traffic_data(traffic_data):
    """
        This encapsulate the filtering and sorting logic and return the filtered and sorted table
    """
    libray = Tables()
    libray.filter_table_by_column(
        table=traffic_data, column=rate_key, operator="<", value=max_rate)
    libray.filter_table_by_column(
        table=traffic_data, column=gender_key, operator="==", value=both_genders)

    libray.sort_table_by_column(
        table=traffic_data, column=year_key, ascending=False)


def transform_the_json_into_table():
    """ 
        The sales data  system expect to receive the traffic data in the below format
       {
         "country": "three-letter-country-code-here",
         "year": 2022,
         "rate": 1.23456
        }

        Looking at the downloaded data, we have to manipulate the data and get the latest available data
        for reach country where:
         -  Three-letter country code (SpatialDim in the raw data)
         - the data concerns both female and male (Dim1 indicate both sexes in the raw data)
         - the rate is average rate (NumericValue in the raw data)
         - the average rate is below 5.0
    """
    # Return contents  in JSON format
    # Documentaion: https://robocorp.com/docs/libraries/rpa-framework/rpa-json
    load_json = JSON()
    new_json = load_json.load_json_from_file(filename=traffic_json_file_path)

    # Convert to table
    # documentation: https://robocorp.com/docs/libraries/rpa-framework/rpa-tables
    library = Tables()
    traffic_data = library.create_table(
        data=new_json["value"])

    # Sort and filter before writing to the table
    filter_and_sort_traffic_data(traffic_data)

    # Write the table to csv
    library.write_table_to_csv(
        table=traffic_data, path="output/test.csv", header=True)


def main():
    try:
        download_traffic_data()
        transform_the_json_into_table()
    except:
        pass


if __name__ == "__main__":
    main()
