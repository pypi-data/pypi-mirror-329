# app_name_placeholder
Template for simple Kortical Cloud model retraining application demo.


### Kortical CLI Configuration
You first need to configure your Kortical CLI tool to be pointing to your system:

`kortical config init`

- \<kortical-platform-url\> is similar to: www.platform.kortical.com/<company_name>/<project_name>
  
(you can find this by looking at your url when you login to the Kortical platform)

### App/Bigquery Configuration

You will need to edit the file `config/app_config.yml`. This should be changed to point to your specific BigQuery table.

Also, you must edit the file `config/service_account_key.json`, this is the service account key for the GCP service account which has access to your BigQuery instance / table. To set this key, run the script `local/bigquery/set_service_account_key.py`.

The BigQuery permissions this account needs are:

- BigQuery Read Session User at the project level (IAM -> Add -> select service account, select BigQuery Read Session User role)
- BigQuery Data Viewer, when looking at the BigQuery explorer UI-> Select table (view actions-> Open) -> share table -> add BigQuery Data Viewer to the same service account

To be able to write to bigquery tables:
- BigQuery MetaData Viewer - at the project level (required to enumerate the datasets)
- BigQuery Data Editor - at the table level (required to write to the table)

Once your service account has the necessary permissions,

 - go to IAM
 - Service Accounts
 - select Manage Keys for that service account (three dots menu)
 - Add Key
 - Copy this key file into the file service_account_key.json inside the bigquery directory of this project.


### App Deployment

There are three apps in this project, which can be found in the `k8s` folder:

* `app_name_placeholder` - this is the main app, which has endpoints for retraining you can communicate with.
* `celery_worker` - this is a background task, where the training workflow takes place.
* `celery_redis` - a database for the celery worker, this stores the current state of a task.

In order for this app to function, you will also need an existing Kortical model; we have assumed a scenario around bookkeeping data, where the model is called `bookkeeping`.

To deploy the app, run the following command from inside the `module_placeholder` directory:

`kortical app deploy --all`


### Local Testing

To run the tests found in the `tests` directory you will need to first install this project into your python environment
From inside the `module_placeholder` directory run:

`pip install -e .`

`pip install wheel`

`pip install -r requirements.txt`

This will run the `setup.py` file and install this project as a module. You will now be able to run:

`pytest tests/` or `pytest -m api` from inside the `module_placeholder` directory on your command line to run the tests.

### Local Debugging

If you are using pycharm as your IDE you can use the tests inside `tests/test_api.py` to debug the project.
You will need to set your python interpreter to the virtual environment with this project installed in (run `pip install -e .` inside this project directory to install this project)
By setting your default test runner to pytest, you will then be able to right click on a test and select `Debug "pytest for test_api..."`
