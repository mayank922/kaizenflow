import logging

import helpers.dbg as dbg
import pandas as pd


_LOG = logging.getLogger(__name__)


def read_csv_range(csv_path, start, nrows, **kwargs):
    """
    Read a specified row range of a csv file and convert to a DataFrame.

    Assumed to have header, which is row 0.

    :param csv_path: Location of csv file
    :param start: First line to read (header is row 0 and is always read)
    :param nrows: Number of non-header rows to read
    :return: DataFrame with columns from csv line 0 (header) and rows
        with lines [start, nrows).
    """
    dbg.dassert_lt(0, start, msg="Row 0 assumed to be header row")
    skiprows = [i for i in range(1, start)]
    df = pd.read_csv(csv_path, skiprows=skiprows, nrows=nrows, **kwargs)
    if df.shape[0] < nrows:
        _LOG.info("Number of df rows = %i vs requested = %i", df.shape[0],
                  nrows)
    return df


def build_chunk(csv_path, col_name, start, nrows_at_a_time=1000, **kwargs):
    """
    Builds a DataFrame from a csv subset as follows:
      - Names the columns using the header line (row 0)
      - Reads the value in (row, col) coordinates (`start`, `col_name`) (if it
          exists) as `value`
      - Adds row `start` and all subsequent contiguous rows with `value` in
          column `col_name`

    For memory efficiency, the csv is processed in chunks of size
    `nrows_at_a_time`.

    :param csv_path: Location of csv file
    :param col_name: Name of column whose values define chunks
    :param start: First row to process
    :param nrows_at_a_time: Size of chunks to process
    :return: DataFrame with columns from csv line 0
    """
    dbg.dassert_lt(0, start)
    stop = False
    dfs = []
    val = read_csv_range(csv_path, start, 1, **kwargs)[col_name].iloc[0]
    _LOG.info('Building chunk for %s', val)
    counter = 0
    while not stop:
        df = read_csv_range(csv_path, start + counter * nrows_at_a_time,
                            nrows_at_a_time)
        # Break if there are no matches.
        if df.shape[0] == 0:
            break
        if not (df[col_name] == val).any():
            break
        # Stop if we have run out of rows to read
        if df.shape[0] < nrows_at_a_time:
            stop = True
        idx_max = (df[col_name] == val)[::-1].idxmax()
        # Stop if we have reached a new value
        if idx_max < (df.shape[0] - 1):
            stop = True
        dfs.append(df.iloc[0:idx_max + 1])
        counter += 1
    return pd.concat(dfs, axis=0).reset_index(drop=True)


def find_first_matching_row(csv_path, col_name, val, start=1,
                            nrows_at_a_time=1000000, **kwargs):
    """
    Find first row in csv where value in column `col_name` equals `val`.

    :param csv_path: Location of csv file
    :param col_name: Name of column whose values define chunks
    :param val: Value to match on
    :param start: First row (inclusive) to start search on
    :param nrows_at_a_time: Size of chunks to process
    :return: Line in csv of first matching row at or past start
    """
    curr = start
    while True:
        _LOG.info("Start of current chunk = line %i", curr)
        df = read_csv_range(csv_path, curr, nrows_at_a_time, **kwargs)
        if df.shape[0] < 1:
            _LOG.info("Value %s not found", val)
            break
        matches = df[col_name] == val
        if matches.any():
            idx_max = matches.idxmax()
            return curr + idx_max
        else:
            curr += nrows_at_a_time
