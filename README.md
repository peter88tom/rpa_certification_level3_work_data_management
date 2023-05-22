# rpa_certification_level3_work_data_management
In thisi course teaches how to:

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