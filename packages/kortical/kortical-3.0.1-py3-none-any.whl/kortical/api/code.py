import yaml


class Code:

    @staticmethod
    def from_file(file_path):
        with open(file_path, 'r') as f:
            return Code(f.read())

    @staticmethod
    def _clean_data(d):
        if isinstance(d, (list, tuple)):
            d = [Code._clean_data(x) for x in d]
            if all([isinstance(x, dict) and len(x) == 1 or isinstance(x, str) for x in d]):
                d = {list(x.keys())[0] if isinstance(x, dict) else x: list(x.values())[0] if isinstance(x, dict) else None for x in d}
        if isinstance(d, dict):
            d = {k: Code._clean_data(v) for k, v in d.items()}
        return d

    @staticmethod
    def _transform_indent(code):
        lines = code.split('\n')
        in_multi_line_string = False
        for i in range(len(lines)):
            if lines[i].endswith(': |'):
                in_multi_line_string = True
                continue
            if in_multi_line_string:
                if 'remove_original_column:' in lines[i]:
                    in_multi_line_string = False
                    continue
                lines[i] = f"  {lines[i]}"
        return '\n'.join(lines)

    def __init__(self, code):
        self.code = code
        # The way PyYaml load requires 4 spaces for block style strings seems to be contrary to
        # the spec https://yaml.org/spec/1.2.2/#61-indentation-spaces so just added a work around
        self.dict = Code._clean_data(yaml.safe_load(self._transform_indent(code)))['ml_solution']
