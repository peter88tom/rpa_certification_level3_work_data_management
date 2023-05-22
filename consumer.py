"""
	Consumes traffic data work items.
"""
from RPA.Robocorp.WorkItems import WorkItems
from RPA.HTTP import HTTP
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
    # http = HTTP()
    # try:
    #     http.POST(
    #         url="https://robocorp.com/inhuman-insurance-inc/sales-system-api", json=payload)
    # except Exception as e:
    #     print(e)
    #     pass

    try:
        r = requests.post(
            url="https://robocorp.com/inhuman-insurance-inc/sales-system-api", json=payload)

        print(r.status_code)
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
        pass


def main():
    try:
        load_work_items()
    except Ellipsis as e:
        print(e)
        pass


if __name__ == "__main__":
    main()
