"""
Produce traffic data work items
"""
from RPA.HTTP import HTTP
import pandas as pd
from RPA.Tables import Tables
from RPA.JSON import JSON
from RPA.Robocorp.WorkItems import WorkItems

# Item work
wi = WorkItems()

# Traffic data API
traffic_data_api = "https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json"

# Path to Json data file after downloding from the API
traffic_json_file_path = "output/traffic.json"
# Path go csv file that


# Varibles for technical names and numbers
max_rate = 5.0
rate_key = "NumericValue"
gender_key = "Dim1"
both_genders = "BTSX"
year_key = "TimeDim"
country_key = "SpatialDim"


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
    # get_latest_data_by_country(traffic_data)

    # Write the table to csv
    library.write_table_to_csv(
        table=traffic_data, path="output/test.csv", header=True)


def get_latest_data_by_country():
    """
        The traffic data is now filtered following the business rules.
        It still contains the data for all available years per country.

        We are only interested in the latest traffic data.

        First, you group the data using the three-letter country code, since
         the data is already sorted descending by year, you can get the first row of 
         each group to get the latest available traffic data for each country.
    """
    data = "output/test.csv"

    table = Tables()
    traffic_data_table = table.read_table_from_csv(path=data)
    traffic_by_country_key = table.group_table_by_column(
        table=traffic_data_table, column=country_key)

    latest_data_by_country = []
    for group in traffic_by_country_key:
        latest_data_by_country.append(table.pop_table_row(group))

    # transfor raw data into business data
    create_work_item_payloads(latest_data_by_country)


def save_work_item_payload(payloads):
    """
        Save the payload as work items.
        Create one work item per API payload

        Documentation: https://robocorp.com/docs/libraries/rpa-framework/rpa-robocorp-workitems
    """
    wi.get_input_work_item()
    for payload in payloads:
        variables = {"traffic_data": payload}
        wi.create_output_work_item(variables=variables, save=True)


def create_work_item_payloads(latest_data_by_country):
    """
        The create work item payloads loops the list of traffic data - essentially rows.
        - For each row, create a new dictionary then append to a payloads dictionary
    """
    payloads = []
    for row in latest_data_by_country:
        payload = {
            "country": row[country_key],
            "year": row[year_key],
            "rate": row[rate_key]
        }

        payloads.append(payload)

    # Save each payload as work item
    save_work_item_payload(payloads)


def main():
    try:
        download_traffic_data()
        transform_the_json_into_table()
        get_latest_data_by_country()
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    main()
