# app_name_placeholder
Template for simple Kortical Cloud chatbot application demo.


### Kortical CLI Configuration
You first need to configure your Kortical CLI tool to be pointing to your system:

`kortical config init`

- \<kortical-platform-url\> is similar to: www.platform.kortical.com/<company_name>/<project_name>
  
(you can find this by looking at your url when you login to the Kortical platform)

### App Configuration

You will need to set some configuration files before deploying the app, these exist within the `config` directory.

### App Deployment
To deploy the app you need to run the following command from inside the `app_name_placeholder` directory:

`kortical app deploy`


### Local Testing

To run the tests found in the `tests` directory you will need to first install this project into your python environment
From inside the `app_name_placeholder` directory run:

`pip install -e .`

`pip install wheel`

`pip install -r requirements.txt`

This will run the `setup.py` file and install this project as a module. You will now be able to run:

`pytest tests/` or `pytest -m api` from inside the `app_name_placeholder` directory on your command line to run the tests.

### Local Debugging

If you are using pycharm as your IDE you can use the tests inside `tests/test_api.py` to debug the project.
You will need to set your python interpreter to the virtual environment with this project installed in (run `pip install -e .` inside this project directory to install this project)
By setting your default test runner to pytest, you will then be able to right click on a test and select `Debug "pytest for test_api..."`
