import io
import os

from kortical.api import advanced
from kortical.helpers.print_helpers import print_success, print_info


class Data:

    @classmethod
    def upload_file(cls, path, targets=None):
        name = os.path.basename(path)
        with open(path) as f:
            print_info(f"Uploading data [{name}]")
            data_id = advanced.data.upload_data(name, f)
        data = cls(data_id, name)
        if targets:
            data.set_targets(targets)
        return data

    @classmethod
    def upload_df(cls, df, name, targets=None):
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        print_info(f"Uploading data [{name}]")
        data_id = advanced.data.upload_data(name, stream)
        data = cls(data_id, name)
        if targets:
            data.set_targets(targets)
        return data

    def __init__(self, data_id, name):
        self.id = data_id
        self.name = name

    def set_targets(self, targets):
        advanced.data.set_targets(self.id, targets)

    def get_code(self, targets=None):
        if targets:
            self.set_targets(targets)
        print_info(f"Generating code for data [{self.id}|{self.name}]")
        return advanced.data.generate_code(self.id)

    def validate_code(self, model_code):
        print_info(f"Validating code for data [{self.id}|{self.name}]")
        errors = advanced.data.validate_code(self.id, model_code)
        if len(errors) > 0:
            errors = [error['msg'] for error in errors]
            formatted_errors = "\t\n".join(errors)
            error_message = f'The platform identified some issues with the model code. ' \
                            f'Please fix these errors and try again:\n\n' \
                            f'{formatted_errors}'
            raise Exception(error_message)
        else:
            print_success("Model code is valid.")
