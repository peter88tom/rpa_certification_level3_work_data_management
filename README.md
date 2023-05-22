# rpa_certification_level3_work_data_management
[Link to the course](https://robocorp.com/docs/courses/work-data-management)

This course teaches us how to:

- Automate a process where the target systems don't have a graphical user interface. No web browsers.
- Structure robot using the `producer-consumer` pattern. The robot will `produce` business data from raw input data and then `consume` that data in small chucks. `work items`.
- Split the robot code into multiple logical pieces instead of single. long wall-of-code. Better readability. 
- Refactor the code constanly to keep it tidy and maintainable when it evolves.
- Extract, Transform, Load - (ETL) business data
- Validate business data and handle business data exceptions using work items.
- Communicate with an (HTTP) API and handle the responses.
- Handle application exceptions using work items.
- Manage work data in Control Room.


# The Robot
We will build the integration of [the road traffic fatality rate API](https://raw.githubusercontent.com/robocorp/inhuman-insurance-inc/main/RS_198.json) and [the insurance sales System](https://robocorp.com/inhuman-insurance-inc/sales-system-api).

The sales API  takes in the traffic data in a specific business format, one entry at a time.

- `producer-consumer` pattern enable to build automation in a way that allows to track status of individual requests and mitigates the risk of everythin falling apart.

- In practice the robot will use [work items](https://robocorp.com/docs/development-guide/control-room/work-items). One task is to generate the sales system API payload from the raw traffic data(the input). The other is to process that data and submit it to the insurance sales system. `Producer->Work Items->Consumer`.

- `Business exception` caused by invalid data, needs manual handling on the exception. If you can this type of exception flag the data for manual inspection.

- `Application exceptions` are any exception cause by technical issues. You can resolve this by retrying actions until they succeed.


# A Producer -> Consumer concept

Implementing a `producer -> consumer` robot you have to split the robot into logical parts. This will help you with updating and maintaining the code easily.

In this robot we have separated the logic into three parts named `producer.py, consumer.py, and shared.py`. We also updated the `robot.yaml` file to call the tasks using thier names.


# Data Filtering, Sorting and Manipulation

In this course we learned different techniques for filtering, sorting and manipulating data from `JSON` file.

Steps that we followed:

- Download data from the remote server using [RPA.HTTP](https://robocorp.com/docs/libraries/rpa-framework/rpa-http) library, and saved it in `.json` format. You can see this in the `producer.py` file.

- We used [RPA.JSON](https://robocorp.com/docs/libraries/rpa-framework/rpa-json) libray to manipulate JSON data and string

- We used [RPA.Tables](https://robocorp.com/docs/libraries/rpa-framework/rpa-tables) library to transform the JSON data into a Table for easier manipulation. Also used this library to filter and sort the data.


When naming varibles remember to use business terms in the code instead of technical terms and numbers.


# About work items

[Work Items](https://robocorp.com/docs/libraries/rpa-framework/rpa-robocorp-workitems) are using for managing data that go through multiple steps and tasks inside a process. Each step of a process receives input work items from previous step, and create output work items for next step.

A work item's data payload is JSON and allows storing anything that is serializable.

In our robot we created work items in a `producer.py` where after cleaning up the data we selected the required data and make them avaible for the next step(`consumer.py`) via work items.

Once you run the producer tast, a `devdata/work-items-out/run-1/work-items.json` file is automatically created. A new run-n folder is created every time you run your robot. Those output work items come in handy later when implementing and testing your consumer robot since they can be used as test input for the consumer 


# Summary of the producer robot(producer.py)

- Downloads the raw traffic data.
- Transforms the raw data into a business data format.
- Saves he business data as work-items that can be consumed later.