"""
	Consumes traffic data work items.
"""
from RPA.Robocorp.WorkItems import WorkItems
import requests

wi = WorkItems()


def process_traffic_data():
    """
        Process each traffic data
    """
    payload = wi.get_work_item_payload()

    validate_traffic_data(payload)


def load_work_items():
    """  Loop through the all work items in a que
        Documentation: https://robocorp.com/docs/courses/work-data-management/loop-the-work-items
    """
    wi.get_input_work_item()
    wi.for_each_input_work_item(process_traffic_data)


def post_traffic_data_to_sales_system(payload):
    """
        Post data to sales system
    """
    try:
        r = requests.post(
            url="https://robocorp.com/inhuman-insurance-inc/sales-system-api", json=payload)

        # Handle a successfuly sales system API response
        if r.status_code == 200:
            wi.release_input_work_item(state="Done")

        # Application error occured
        wi.release_input_work_item(
            state="FAILED", exception_type="APPLICATION", code="TRAFFIC_DATA_POST_FAILED",
            message=f"This traffic_data has failed: {payload}")
    except Exception as e:
        print(e)
        pass


def validate_traffic_data(payload):
    """
        Validate traffic data before feeding to the sales system
        Documentation: https://robocorp.com/docs/courses/work-data-management/validate-business-data
    """
    if len(payload['traffic_data']['country']) == 3:
        post_traffic_data_to_sales_system(payload)
    else:
        # Business error occured, inform
        wi.release_input_work_item(
            state="FAILED", exception_type="BUSINESS", code="INVALID_TRAFIC_DATA", message=f"Invalid traffic data{payload}")


def main():
    try:
        load_work_items()
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    main()
