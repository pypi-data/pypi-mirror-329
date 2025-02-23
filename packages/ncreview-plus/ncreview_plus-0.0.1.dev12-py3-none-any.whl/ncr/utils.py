'''A few miscellaneous functions and objects used by the datastream and
datastreamdiff modules.
'''
import re
import time
import numpy as np
import datetime as dt
import calendar
import xarray as xr
from pdb import set_trace
from os.path import basename

from . import colorformat as cf

class ParsedNcFilename:
    cdf_extensions = ['nc', 'cdf']
    yyyymmdd_pattern = re.compile(r'^(\d{4})(\d\d)(\d\d)$')
    hhmmss_pattern = re.compile(r'^([0-2]\d)([0-5]\d)([0-5]\d)$')
    printed_invalid_datestamp_warning = False
    printed_no_datestamp_warning = False

    def __init__(self, path:str, datestamp_format:str='%Y%m%d', datastream_pattern:str=None):
        self.path = path
        self.filename = basename(path)
        self.is_cdf_file = False
        self.datastream_name = None

        self.year = None
        self.month = None
        self.day = None

        self.hour = None
        self.minute = None
        self.second = None

        self.timestamp_values = None
        self.datetime = None

        self.parse_filename()

    def parse_filename(self):
        filename_tokens = self.filename.split('.')
        if filename_tokens[-1] not in ParsedNcFilename.cdf_extensions:
            return
        
        self.is_cdf_file = True

        date_match_indices = []
        date_matches = []
        time_match_indices = []
        time_matches = []
        for i in range(len(filename_tokens) - 1):
            date_match = ParsedNcFilename.yyyymmdd_pattern.match(filename_tokens[i])
            time_match = ParsedNcFilename.hhmmss_pattern.match(filename_tokens[i])
            if date_match:
                date_matches.append(date_match)
                date_match_indices.append(i)
            if time_match:
                time_matches.append(time_match)
                time_match_indices.append(i)
        
        date_match = None
        time_match = None
        # If we find no timestamp,
        # assume the ds name is everything except the extension
        self.datastream_name = '.'.join(filename_tokens[:-1])

        # Allowed format: begin datestamp, begin and end datestamp
        # Assumptions:
        # - if there are two datestamps, the begin datestamp appears first
        # - if there are more than two datestamps, we accidentally matched unrelated data
        #   and should bail out
        # - timestamps are useless unless we also have a datestamp
        if len(date_match_indices) > 2:
            if not ParsedNcFilename.printed_invalid_datestamp_warning:
                error_message = f"WARNING: Could not identify datestamp in filename {self.filename}\n"
                error_message+= f'(candidates:'
                for index in date_match_indices:
                    error_message += f' "{filename_tokens[i]}"'
                error_message += ')\n'
                error_message += "Date-based file filtering will be much slower."
                print(error_message)
                ParsedNcFilename.printed_invalid_datestamp_warning = True

        elif len(date_match_indices) == 0:
            if not ParsedNcFilename.printed_no_datestamp_warning:
                print(f"WARNING: No datestamp found in filename {self.filename}; " +
                      "date-based file filtering will be much slower.")
                ParsedNcFilename.printed_no_datestamp_warning = True

        else:
            date_match = filename_tokens[date_match_indices[0]]
            self.year, self.month, self.day = [
                int(val) for val in date_matches[0].groups()]
            
            if len(time_match_indices) == 1:
                time_match = filename_tokens[time_match_indices[0]]
                self.hour, self.minute, self.second = [
                    int(val) for val in time_matches[0].groups()]
            else:
                self.hour, self.minute, self.second = [0, 0, 0]
            self.timestamp_values = [self.year, self.month, self.day, 
                self.hour, self.minute, self.second]

            # Datastream name: everything except the extension and the timestamps
            date_and_time_indices = date_match_indices + time_match_indices
            for i in range(len(date_and_time_indices)):
                filename_tokens.pop(date_and_time_indices[i])
                for j in range(i, len(date_and_time_indices)):
                    if date_and_time_indices[j] > date_and_time_indices[i]:
                        date_and_time_indices[j] -= 1
            self.datastream_name = '.'.join(filename_tokens[:-1])

    # Formula for determining ds name of a file:
    # 
        

    def file_datastream(self):
        return self.datastream_name

    def file_time(self, time_varname:str='time', base_time_varname:str='base_time',
                  time_offset_varname:str='time_offset'):
        if self.datetime is None and self.timestamp_values is not None:
            self.datetime = dt.datetime(*self.timestamp_values) 
        if self.datetime:
            return self.datetime
        
        try:
            with xr.open_dataset(self.path) as ds:
                if time_varname in ds.data_vars:
                    self.datetime = ds.time.data[0]
                elif (base_time_varname in ds.data_vars and 
                      time_offset_varname in ds.data_vars):
                    self.datetime = ds[base_time_varname].data + ds[time_offset_varname].data[0]

                if self.datetime is not None:
                    self.datetime = self.datetime.astype('datetime64[s]').astype('int64')
                    self.datetime = dt.datetime.fromtimestamp(self.datetime)
                return self.datetime
        except:
            return None

    def __lt__(self, other):
        return self.filename < other.filename

def strtotime(timestring, timeformat):
    t = time.strptime(timestring, timeformat)
    return calendar.timegm(t)


def timetostr(timestamp, timeformat):
    return time.strftime(timeformat, time.gmtime(timestamp))


# This functionality exists in the standard library through functools.lru_cache
# starting in version 3.2.
def store_difference(func):
    '''Decorator that causes difference() methods to store and reuse their result.
    '''
    def difference(self):
        if not hasattr(self, '_difference'):
            setattr(self, '_difference', func(self))
        return self._difference
    return difference


def json_section(self, contents):
    '''Returns a json section object with the specified contents.
    '''
    sec = {
        'type': 'section',
        'name': self.name,
        'contents': contents
    }
    if hasattr(self, 'difference'):
        sec['difference'] = self.difference()
    elif hasattr(self, '_difference'):
        sec['difference'] = self._difference
    return sec


def JEncoder(obj):
    ''' Defines a few default behaviours when the json encoder doesn't know
    what to do
    '''
    try:
        if np.isnan(obj):
            return None
        elif obj // 1 == obj:  # loses precision after about 15 decimal places
            return int(obj)
        else:
            return float(obj)
    except:  # noqa: E722
        try:
            return str(obj)
        except:  # noqa: E722
            raise TypeError(
                cf.setError((
                    'Object of type {0} with value {1} is not JSON ' +
                    'serializable'
                ).format(type(obj), repr(obj)))
            )


def join_times(old_ftimes, new_ftimes, union=False):
    '''Yields time intervals shared by both the old and new files, in order.

    Parameters:
        old_ftimes  list of old file times as TimeInterval objects
        new_ftimes  list of new file times as TimeInterval objects

    Yields:
        yields the tuple:
            beg    beginning of the shared time interval
            end    end of the shared time interval
            old_i  index of interval in old_ftimes that overlaps this shared
                   interval
            new_i  index of interval in new_ftimes that overlaps this shared
                   interval
    '''
    old_itr = iter(enumerate(old_ftimes))
    new_itr = iter(enumerate(new_ftimes))

    old_i, old_f = next(old_itr, (None, None))
    new_i, new_f = next(new_itr, (None, None))

    if union:
        while old_f or new_f:
            beg = old_f.beg if old_f else None
            if beg is None or (new_f and new_f.beg < beg):
                beg = new_f.beg
            end = old_f.end if old_f else None
            if end is None or (new_f and new_f.end < end and new_f.beg < end):
                end = new_f.end

            yield (
                beg,
                end,
                old_i if (
                    old_f and old_f.end > beg and old_f.beg < end
                ) else None,
                new_i if (
                    new_f and new_f.end > beg and new_f.beg < end
                ) else None
            )

            if old_f and old_f.beg < end:
                old_i, old_f = next(old_itr, (None, None))
            if new_f and new_f.beg < end:
                new_i, new_f = next(new_itr, (None, None))
        return

    while old_f and new_f:
        beg = max(old_f.beg, new_f.beg)
        end = min(old_f.end, new_f.end)

        if beg < end:
            yield beg, end, old_i, new_i

        if old_f.end < new_f.end:
            old_i, old_f = next(old_itr, (None, None))
        elif old_f.end > new_f.end:
            new_i, new_f = next(new_itr, (None, None))
        else:
            old_i, old_f = next(old_itr, (None, None))
            new_i, new_f = next(new_itr, (None, None))


def time_diff(n):
    # unnecessary parentheses around assignments
    (m, s) = divmod(n, 60)
    (h, m) = divmod(m, 60)
    if h > 23:
        (d, h) = divmod(h, 24)
        return '%dd:%02dh:%02dm:%02ds' % (d, h, m, s)
    return '%dh:%02dm:%02ds' % (h, m, s)
