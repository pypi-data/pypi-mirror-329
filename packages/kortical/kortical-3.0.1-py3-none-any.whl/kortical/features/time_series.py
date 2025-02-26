"""
    Copyright 2020, Kortical Ltd - All Rights Reserved
    Unauthorized copying of this file, via any medium is strictly prohibited
    Proprietary and confidential
    Written by Kortical Ltd
"""
import numbers
from collections import OrderedDict
from datetime import date, datetime, timedelta
from enum import Enum, auto
from functools import partial, update_wrapper
import multiprocessing as mp
import os

from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from tqdm import tqdm

from kortical.helpers.pandas_helpers import is_day_first

# Constants
# Number of parallel workers to use during row generation
NUM_PARALLEL_WORKERS = os.cpu_count()

start_methods = mp.get_all_start_methods()
# Windows only supports spawn as a start method, so use that if forkserver is not available
start_method = 'forkserver' if 'forkserver' in start_methods else 'spawn'

# Divide row generation sufficiently to ensure workers are kept busy
MIN_TASKS_PER_WORKER = 5

# Limit number of rows per parallel task to ensure the user sees a decent progress indicator
MAX_ROWS_PER_TASK = 1000


# Standard functions
def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func


class Functions:
    max = np.max
    mean = np.mean
    median = np.median
    min = np.min
    std = wrapped_partial(np.std, ddof=1)       # Default params changed to match pandas default behaviour
    sum = np.sum


# Ignore time component
class IgnoreTimeComponent(Enum):
    NONE = auto()
    HOUR = auto()
    MINUTE = auto()
    SECOND = auto()


def _ignore_time_component(datetime, ignore):
    if ignore == IgnoreTimeComponent.HOUR:
        datetime = datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif ignore == IgnoreTimeComponent.MINUTE:
        datetime = datetime.replace(minute=59, second=59, microsecond=999999)
    elif ignore == IgnoreTimeComponent.SECOND:
        datetime = datetime.replace(second=59, microsecond=999999)

    return datetime


class TimeWindow(object):

    def __init__(self, start, duration, offset=None, use_value_as_is=False):
        """Create a time window for a time series.

        :param start:           the start time delta, either relative to the start of the series or an absolute time
        :param duration:        the duration of the time window or an absolute time
        :param offset:          to add a fixed time offset, add that here
        :param use_value_as_is: do not apply functions to the data within this time window; instead, just copy the first
                                value in the window to the result. Intended to be used with daily lags where it doesn't
                                make sense to apply functions to a single daily value.
        :returns:               a TimeWindow
        """
        assert isinstance(start, (date, datetime, timedelta, relativedelta))
        assert isinstance(duration, (date, datetime, timedelta, relativedelta))
        assert not offset or isinstance(offset, timedelta)
        self.start = start
        self.duration = duration
        self.offset = offset
        self.use_value_as_is = use_value_as_is

        # Pre-compute time bounds for the case where absolute datetimes are used
        self._precomputed_time_bounds = None
        if isinstance(self.start, datetime):
            if isinstance(self.duration, datetime):
                self._precomputed_time_bounds = \
                    datetime.max(self.start, self.duration), datetime.min(self.start, self.duration)
            else:
                self._precomputed_time_bounds = self.start, self.start - self.duration

    def get_start_bound(self, time0):
        if self._precomputed_time_bounds:
            return self._precomputed_time_bounds[0]
        else:
            start = time0 - self.start

            if self.offset:
                start += self.offset

            return start

    def get_end_bound(self, start_bound):
        if self._precomputed_time_bounds:
            return self._precomputed_time_bounds[1]
        else:
            return start_bound - self.duration

    def get_time_bounds(self, time0):
        start = self.get_start_bound(time0)
        end = self.get_end_bound(start)
        return (start, end)

    @staticmethod
    def _get_if_only_one_property_is_set(time):
        property = None
        for k, v in time.__dict__.items():
            if isinstance(v, numbers.Number) and k != '_has_time':
                if v != 0:
                    if property is None:
                        property = k
                    else:
                        return 'more_than_one'
        return property

    @staticmethod
    def _get_string_representation_of_time(time):
        if isinstance(time, (date, datetime)):
            return f'{time}'
        if isinstance(time, timedelta):
            if time.total_seconds() == 0.0:
                return 'now'
            # Check if it's exactly a week
            if time.total_seconds() % (7 * 24 * 60 * 60) == 0:
                return f'{time.days // 7}w'
            if time.total_seconds() % (24 * 60 * 60) == 0:
                return f'{time.days}d'
            if time.total_seconds() % (60 * 60) == 0:
                return f'{time.total_seconds() // (60 * 60):.0f}h'
            if time.total_seconds() % 60 == 0:
                return f'{time.total_seconds() // 60:.0f}m'
            if time.microseconds == 0 and time.days == 0:
                return f'{time.seconds}s'
            if time.seconds == 0 and time.days == 0:
                return f'{time.microseconds}us'
            return f'{time.total_seconds()}s'
        if isinstance(time, relativedelta):
            time_property = TimeWindow._get_if_only_one_property_is_set(time)

            time_property_map = {
                'microseconds': 'us',
                'seconds': 's',
                'minutes': 'm',
                'hours': 'h',
                'days': 'd',
                'weeks': 'w',
                'months': 'm',
                'years': 'y',
            }

            if time_property is None:
                return 'now'
            if time_property in time_property_map:
                return f'{time.__getattribute__(time_property)}{time_property_map[time_property]}'
            return f'?'

    @property
    def name(self):
        if self.use_value_as_is:
            return f'{self._get_string_representation_of_time(self.start)}'
        elif isinstance(self.start, (date, datetime)):
            return f'start_{self._get_string_representation_of_time(self.start)}_duration_{self._get_string_representation_of_time(self.duration)}'
        else:
            return f'start_in_{self._get_string_representation_of_time(self.start)}_duration_{self._get_string_representation_of_time(self.duration)}'


# Standard windows
def generate_daily_windows(num_days, start_offset=None):
    start_offset = start_offset if start_offset else timedelta()
    return [
        TimeWindow(
            start=start_offset + timedelta(days=i),
            duration=timedelta(days=1),
            use_value_as_is=True
        ) for i in range(num_days)
    ]


def generate_weekly_windows(num_weeks, start_offset=None):
    start_offset = start_offset if start_offset else timedelta()
    return [
        TimeWindow(
            start=start_offset + timedelta(weeks=i),
            duration=timedelta(weeks=1)
        ) for i in range(num_weeks)
    ]


def generate_monthly_windows(num_months, start_offset=None):
    start_offset = start_offset if start_offset else relativedelta()
    return [
        TimeWindow(
            start=start_offset + relativedelta(months=i),
            duration=relativedelta(months=1),
        ) for i in range(num_months)
    ]


def generate_yearly_windows(num_years, start_offset=None):
    start_offset = start_offset if start_offset else relativedelta()
    return [
        TimeWindow(
            start=start_offset + relativedelta(years=i),
            duration=relativedelta(years=1)
        ) for i in range(num_years)
    ]


lags_daily_over_10_days = generate_daily_windows(num_days=10)
lags_weekly_over_3_weeks = generate_weekly_windows(num_weeks=3)
lags_monthly_over_3_months = generate_monthly_windows(num_months=3)
lags_monthly_over_6_months = generate_monthly_windows(num_months=6)
lags_yearly_over_3_years = generate_yearly_windows(num_years=3)

lags_daily_over_10_days_last_year = generate_daily_windows(
    num_days=10,
    start_offset=relativedelta(years=1)
    )
lags_weekly_over_3_weeks_last_year = generate_weekly_windows(
    num_weeks=3,
    start_offset=relativedelta(years=1)
    )

lags_default_daily = lags_daily_over_10_days + lags_weekly_over_3_weeks + lags_monthly_over_3_months
lags_default_monthly = lags_monthly_over_6_months


# Data preparation
def _prepare_dataframe(dataframe, datetime_column, datetime_format, columns, id_columns=None):
    df = dataframe

    # Convert datetime values to datetime objects and set as the dataframe index
    if datetime_format:
        df[datetime_column] = pd.to_datetime(df[datetime_column], format=datetime_format, cache=True)
    else:
        is_day_first_ = is_day_first(df[datetime_column])
        df[datetime_column] = pd.to_datetime(df[datetime_column], infer_datetime_format=True, cache=True, dayfirst=is_day_first_)
    df.index = df[datetime_column]
    del df[datetime_column]

    # Convert all specified columns (on which we will calculate lags etc.) to float
    for c in columns:
        df[c] = df[c].astype('float64', copy=False)

    # Sort the dataframe rows into the most appropriate order for efficient processing later
    if not id_columns:
        # Sort by datetime descending
        dataframe.sort_index(ascending=False, inplace=True)
    else:
        # Sort by id columns ascending, datetime descending
        dataframe.sort_values(by=id_columns + [datetime_column], ascending=[True] * len(id_columns) + [False], inplace=True)

    return df


def _resample(dataframe, rule, aggregations):
    df = dataframe
    df = df.resample(rule).agg(aggregations)

    # Resampling will switch the dataframe to ascending order (oldest timestamps first)
    # Sort again in descending order to match the case when no resampling is done.
    #
    # We do not include id column in the sort because resampling is always done within an id column group.
    # Therefore, all rows within this dataframe will share the same id column values.
    df.sort_index(ascending=False, inplace=True)

    return df


# Column naming
def _make_column_names(time_windows, columns, functions):
    column_names = []

    for (wdx, window) in enumerate(time_windows):
        window_str = window.name if window.name is not None else f'window{wdx}'

        for col in columns:
            if window.use_value_as_is:
                col_name = f'{col}_{window_str}' if window_str else col
                column_names.append(col_name)
            else:
                if isinstance(functions, (list, tuple)):
                    for func in functions:
                        col_name = f'{col}_{func.__name__}'
                        if window_str:
                            col_name += f'_{window_str}'
                        column_names.append(col_name)
                else:
                    raise Exception("functions needs to be a function or a list of functions")

    return column_names


# Feature creation
def _create_features(time0, dataframe, columns, time_windows, functions):
    # Prep for performance optimisation
    #  - Provide datetime index in ascending order for efficient binary searches
    #  - Extract column data into numpy arrays once for faster processing of time windows
    ascending_index = dataframe.index[::-1]
    len_index = len(ascending_index)
    column_to_numpy_map = {}
    for column in columns:
        column_to_numpy_map[column] = dataframe[column].to_numpy()

    # Build features for each time window
    features = []
    for time_window in time_windows:
        if time_window.use_value_as_is:
            # Just use start time to find the single element to include - no functions applied
            start_time = time_window.get_start_bound(time0)
            start_idx = len_index - ascending_index.searchsorted(start_time, side='right')
            for (cdx, column_name) in enumerate(columns):
                column = column_to_numpy_map[column_name]
                if start_idx < len(column):
                    features.append(column[start_idx])
                else:
                    features.append(np.nan)
        else:
            # Find all values within the bounds of the window and apply the functions to them
            start_time, end_time = time_window.get_time_bounds(time0)
            start_idx = len_index - ascending_index.searchsorted(start_time, side='right')
            end_idx = len_index - ascending_index.searchsorted(end_time, side='right')

            if start_idx != end_idx:
                for (cdx, column_name) in enumerate(columns):
                    column = column_to_numpy_map[column_name][start_idx:end_idx]

                    # Drop NaNs from the column now so we can apply non-NaN versions of functions,
                    # which is more efficient than applying NaN versions of each function (as each
                    # function has to independently check that each value is not a NaN)
                    valid_indices = np.isfinite(column)
                    if len(valid_indices) < len(column):
                        # We have some NaN values to drop
                        column = column[valid_indices]

                    for (fdx, function) in enumerate(functions):
                        features.append(function(column))
            else:
                features.extend(np.full(len(columns) * len(functions), np.nan))

    return features


def create_rows(
        dataframe,
        datetime_column,
        columns,
        time_windows,
        functions,
        sample_frequency,
        datetime_format=None,
        id_columns=None,
        resample_rule=None,
        resample_aggregations=None,
        ignore=IgnoreTimeComponent.HOUR
    ):
    """
    Creates observation first rows for the given time windows at a given sample frequency

    :param dataframe:               input dataframe
    :param datetime_column:         the column which has the datetime index
    :param columns:                 the column(s) which contain numeric values which vary over time
    :param time_windows:            a list of time windows to apply
    :param functions:               list of functions to apply across time windows
    :param sample_frequency:        how often to create an observation (eg daily, monthly, weekly) as time delta
    :param datetime_format:         the format of the datetime values in datetime_column, defined in terms of the directives
                                    described at https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior.
                                    If not provided, uses pandas.to_datetime() to infer the format. Performance can be significantly
                                    better if the format is explicitly provided.
    :param id_columns:              id or ids to differentiate between different time series objects (eg machine id, part number or site id)
    :param resample_rule:           resample rule passed to pandas.DataFrame.resample()
    :param resample_aggregations:   resample aggregations passed to pandas.DataFrame.resample().agg()
    :param ignore:                  if you need to ignore part of the time component, specify that here

    :return:                        dataframe containing the generated rows
    """
    start_time = datetime.utcnow()

    # Check arguments
    assert isinstance(ignore, IgnoreTimeComponent)

    if isinstance(time_windows, TimeWindow):
        time_windows = (time_windows,)

    if id_columns and not isinstance(id_columns, list):
        id_columns = [id_columns]

    if not isinstance(columns, (list, tuple)):
        columns = [columns]

    if callable(functions):
        functions = [functions]

    print("\n\nPreparing dataframe...")
    dataframe = _prepare_dataframe(dataframe, datetime_column, datetime_format, columns, id_columns)

    # Create group -> dataframe map, including doing any required resampling
    group_to_dataframe_map = OrderedDict()
    group_to_result_map = OrderedDict()
    if id_columns:
        for group_name, df_subset in dataframe.groupby(id_columns):
            if resample_rule and resample_aggregations:
                df_subset = _resample(df_subset, resample_rule, resample_aggregations)
            group_to_dataframe_map[group_name] = df_subset
            group_to_result_map[group_name] = []
    else:
        if resample_rule and resample_aggregations:
            dataframe = _resample(dataframe, resample_rule, resample_aggregations)

        # No id columns => use empty group name
        group_name = ''
        group_to_dataframe_map[group_name] = dataframe
        group_to_result_map[group_name] = []

    # Create tasks to be run in parallel
    print("\nSplitting into chunks for parallel processing...")
    tasks = _create_tasks(group_to_dataframe_map, columns, time_windows, functions, sample_frequency, ignore)

    # Execute tasks on worker pool
    print("\nGenerating rows in parallel...")
    _execute_tasks(tasks, group_to_result_map)

    # Combine results into a single set of rows
    all_rows = []
    for (group, rows) in group_to_result_map.items():
        # Sort all rows for group into reverse date order, since the parallel processing mixes up the order
        rows.sort(key=lambda x: x[0], reverse=True)
        all_rows.extend(rows)

    # Get columns names and create a proper dataframe
    print("\n\nRows generated, creating output dataframe...")
    column_names = _make_column_names(time_windows, columns, functions)
    if id_columns:
        column_names = id_columns + column_names
    column_names.insert(0, datetime_column)
    df = pd.DataFrame(all_rows, columns=column_names)
    df.set_index(datetime_column, inplace=True)

    duration = datetime.utcnow() - start_time
    print('\nRow creation complete')
    print(f'Total time: {duration}')

    print('\nTime windows')
    for (wdx, window) in enumerate(time_windows):
        print(f'window{wdx}: start [{window.start}], duration [{window.duration}]')

    return df


# Parallel row generation
class CreateRowsTask:
    def __init__(self, group, sample_datetimes, dataframe, columns, time_windows, functions):
        self.group = group
        self.sample_datetimes = sample_datetimes
        self.dataframe = dataframe
        self.columns = columns
        self.time_windows = time_windows
        self.functions = functions


def _chunks(l, n):
    """ Yield successive n-sized chunks from l """
    for i in range(0, len(l), n):
        yield l[i:i + n]


def _create_tasks(group_to_dataframe_map, columns, time_windows, functions, sample_frequency, ignore):
    # Determine what sample datetimes we will need for each group
    group_to_samples_map = {}
    for (group, dataframe) in tqdm(group_to_dataframe_map.items()):
        index = dataframe.index
        sample_datetimes = []
        sample_datetime = _ignore_time_component(index[0], ignore)
        end_datetime = index[-1]

        while sample_datetime >= end_datetime:
            sample_datetimes.append(sample_datetime)
            sample_datetime -= sample_frequency
            sample_datetime = _ignore_time_component(sample_datetime, ignore)

        group_to_samples_map[group] = sample_datetimes

    # Calculate best guess at the ideal task size
    total_rows = sum(len(sample_list) for sample_list in group_to_samples_map.values())
    min_tasks = NUM_PARALLEL_WORKERS * MIN_TASKS_PER_WORKER
    max_rows_per_task = max(1, int(min(total_rows / min_tasks, MAX_ROWS_PER_TASK)))

    # Create tasks to cover row generation for all groups
    tasks = []
    for (group, dataframe) in group_to_dataframe_map.items():
        # Only include the columns of interest
        df = dataframe[columns]

        for chunk in _chunks(group_to_samples_map[group], max_rows_per_task):
            tasks.append(CreateRowsTask(group, chunk, df, columns, time_windows, functions))

    return tasks


def _execute_tasks(tasks, group_to_result_map):
    context = mp.get_context(start_method)
    pool = context.Pool(NUM_PARALLEL_WORKERS)
    try:
        for (group, task_rows) in tqdm(pool.imap_unordered(_execute_task, tasks), total=len(tasks)):
            group_to_result_map[group].extend(task_rows)
    finally:
        pool.close()
        pool.join()

    return group_to_result_map


def _execute_task(task):
    rows = []
    id_cells = np.atleast_1d(task.group).tolist() if task.group else []
    for sample_datetime in task.sample_datetimes:
        rows.append([sample_datetime] + id_cells + _create_features(sample_datetime, task.dataframe, task.columns, task.time_windows, task.functions))

    return (task.group, rows)