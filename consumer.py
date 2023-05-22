"""
	Consumes traffic data work items.
"""
from RPA.Robocorp.WorkItems import WorkItems
from RPA.HTTP import HTTP


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


def validate_traffic_data(payload):
    """
        Validate traffic data before feeding to the sales system
        Documentation: https://robocorp.com/docs/courses/work-data-management/validate-business-data
    """
    if len(payload['traffic_data']['country']) == 3:
        print("Post to sales system")
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
