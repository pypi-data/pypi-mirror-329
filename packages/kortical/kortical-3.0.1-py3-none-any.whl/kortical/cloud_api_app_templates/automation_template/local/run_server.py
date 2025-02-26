import os
import module_placeholder.main
from kortical.app import get_app_config

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']

if __name__ == '__main__':
    print(f"Paste the following into your browser to access the app:\n\n[http://127.0.0.1:5000?api_key={api_key}]")
    os.environ['SERVER_RUNNING_LOCALLY'] = "TRUE"
    module_placeholder.main.app.run(debug=True)
