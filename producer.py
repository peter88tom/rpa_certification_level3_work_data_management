"""
Produce traffic data work items
"""
from RPA.HTTP import HTTP

# Traffic data end-point
traffic_data = "https://github.com/robocorp/inhuman-insurance-inc/raw/main/RS_198.json"


def download_traffic_data():
    """ Download the trafic data """
    http = HTTP()
    http.download(url=traffic_data, overwrite=True,
                  target_file="output/traffic.json")


def main():
    try:
        download_traffic_data()
    except:
        pass


if __name__ == "__main__":
    main()
