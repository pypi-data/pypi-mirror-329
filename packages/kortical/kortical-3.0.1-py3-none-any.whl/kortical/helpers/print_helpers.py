import colorama
from datetime import datetime
from enum import Enum
import re
import shutil
from texttable import Texttable

from kortical.helpers import KorticalKnownException


def print_success(message: str):
    print(format_success(message))


def print_info(message: str, **kwargs):
    print(format_info(message), **kwargs)


def print_title(message: str):
    print(format_title(message))


def print_question(message: str):
    print(format_question(message))


def print_warning(message: str):
    print(format_warning(message))


def print_error(message: str):
    print(format_error(message))


def format_success(message: str):
    return colorama.Fore.LIGHTGREEN_EX + colorama.Style.BRIGHT + message + colorama.Style.RESET_ALL


def format_info(message: str):
    return colorama.Fore.CYAN + colorama.Style.BRIGHT + message + colorama.Style.RESET_ALL


def format_title(message: str):
    return colorama.Fore.WHITE + colorama.Style.BRIGHT + message + colorama.Style.RESET_ALL


def format_question(message: str):
    return colorama.Fore.MAGENTA + colorama.Style.BRIGHT + message + colorama.Style.RESET_ALL


def format_warning(message: str):
    return colorama.Fore.LIGHTYELLOW_EX + colorama.Style.BRIGHT + message + colorama.Style.RESET_ALL


def format_error(message: str):
    return colorama.Fore.RED + colorama.Style.BRIGHT + message + colorama.Style.RESET_ALL


def strip_colour(message):
    # 7-bit C1 ANSI sequences
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)
    result = ansi_escape.sub('', message)

    return result


def user_prompt_yes_no(message):
    response = input(format_question(message))
    if not response or response.lower() not in ['y', 'yes']:
        return False
    return True


def get_list(items):
    if not isinstance(items, (list, tuple)):
        items = [items]

    if len(items) == 0:
        return "\tNo entries"
    else:
        table = Texttable(max_width=shutil.get_terminal_size().columns)
        columns = [x for x in vars(items[0]).keys() if not x.startswith('_')]
        rows = [columns]
        for item in items:
            values = []
            for value in vars(item).values():
                if isinstance(value, datetime):
                    value = value.strftime("%Y/%m/%d %H:%M:%S")
                elif isinstance(value, Enum):
                    value = value.value
                values.append(value)
            rows.append(values[:len(columns)])

        table.add_rows(rows)
        return table.draw()


def display_list(items):
    print_info(get_list(items))


def display_string_list(header, items):
    if not isinstance(items, (list, tuple)):
        items = [items]

    if len(items) == 0:
        print_info("\tNo entries")
    else:
        table = Texttable(max_width=shutil.get_terminal_size().columns)
        rows = [[x] for x in items]
        rows.insert(0, [header])

        table.add_rows(rows)
        print_info(table.draw())


def user_prompt_input(message):
    print_question(message)
    return input()


def user_prompt_option(message, options):
    choice = user_prompt_input(message)

    if isinstance(options, dict):
        choice = options.get(choice)
        if choice is None:
            print_error("Invalid option.")
            choice = user_prompt_option(message, options)
    elif isinstance(options, list):
        if choice not in options:
            print_error("Invalid option.")
            choice = user_prompt_option(message, options)

    return choice


def print_options(message, index_map):
    print_info(message)
    print()
    for index, template in index_map.items():
        print_info(f"\t[{index}] {template}")
    print()
