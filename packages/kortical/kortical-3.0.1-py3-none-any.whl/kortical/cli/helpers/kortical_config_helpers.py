from kortical.helpers.print_helpers import print_title, display_list


class KorticalConfigRow:

    def __init__(self, key, value, inherited):
        self.key = key
        if isinstance(value, bool):
            self.value = self._bool_to_str(value)
        else:
            self.value = value
        self.inherited = self._bool_to_str(inherited)

    def _bool_to_str(self, value):
        return 'true' if value else 'false'


def get_full_kortical_config(item):
    kortical_config, kortical_config_inherited = item.get_kortical_config()
    kortical_config_full = kortical_config_inherited
    kortical_config_full.update(kortical_config)
    return kortical_config_full


def display_kortical_config_list(item):
    kortical_config, kortical_config_inherited = item.get_kortical_config()
    kortical_config_full = kortical_config_inherited
    kortical_config_full.update(kortical_config)
    kortical_config_rows = [KorticalConfigRow(k, v, k not in kortical_config) for k, v in kortical_config_full.items()]
    print_title(f"Kortical Config for [{item.name}]:")
    display_list(kortical_config_rows)
