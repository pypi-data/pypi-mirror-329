# time_utils.py: converting from/to arrow time strings, using the client timezone

import arrow
import datetime

# don't change these or we won't be able to read old job/run time correctly
date_time_separator = " "
arrow_format_str = 'YYYY-MM-DD HH:mm:ssZZ'

def get_local_timezone():
    # get local timezone as hours from UTC (more reliable than a timezone name)
    tz_hours = datetime.datetime.now().astimezone().utcoffset().total_seconds()/3600
    #print("Local timezone: ", tz_hours)

    atz_hours = abs(tz_hours)
    sign = "+" if tz_hours >= 0 else "-"
    mins = int(atz_hours - int(atz_hours)) * 60
    portable_tz = "UTC{}{}:{:02d}".format(sign, int(atz_hours), mins)
    return portable_tz

def flip_timezone_sign(tz):
    # toggle sign
    if "+" in tz:
        linux_utc = tz.replace("+", "-")
    else:
        linux_utc = tz.replace("-", "+")
    return linux_utc

def get_arrow_str_from_time(time: float):

    # convert time as float to arrow time string
    at = arrow.get(time)

    # add timezone
    at = at.to('local')

    # add our slightly easier to read formatting
    sat = at.format(arrow_format_str)

    return sat

def get_arrow_now_str():
    ''' 
    returns NOW as an arrow time string
    '''
    at = arrow.now()
    sat = at.format(arrow_format_str)
    return sat

def get_time_from_arrow_str(arrow_time_str):
    '''
    converts an arrow time string to seconds (float)
    '''
    if isinstance(arrow_time_str, str):
        ats = arrow_time_str.replace(date_time_separator, "T", 1)
        atime = arrow.get(ats)

    else:
        # some callers pass in a float
        atime = arrow.get(arrow_time_str)

    return atime.datetime.timestamp()

def get_arrow_from_arrow_str(arrow_time_str):
    '''
    converts an arrow time string to arrow time object (float)
    '''
    if isinstance(arrow_time_str, str):
        ats = arrow_time_str.replace(date_time_separator, "T", 1)
        atime = arrow.get(ats)

    else:
        # some callers pass in a float
        atime = arrow.get(arrow_time_str)

    return atime

def parse_time(arrow_time_str):
    '''
    parse an datetime string produced by arrow module
    and return value in form of datetime object. 
    '''
    ats = arrow_time_str.replace(date_time_separator, "T", 1)
    atime = arrow.get(ats)
    dt = atime.datetime
    return dt

def time_diff(time1, time2):
    '''
    Args:
        time1, time2: datetime or arrow objects 
    '''
    atype = arrow.arrow.Arrow
    dttype = datetime.datetime

    # support mixed types
    if type(time1) != type(time2):

        # convert both to datetime without timezone
        if isinstance(time1, atype):
            time1 = time1.datetime.replace(tzinfo=None)

        if isinstance(time2, atype):
            time2 = time2.datetime.replace(tzinfo=None)

    return (time1 - time2).total_seconds()

def elapsed_time(start):
    diff = datetime.datetime.now() - start

    elapsed = str(diff)
    index = elapsed.find(".")
    if index > -1:
        elapsed = elapsed[0:index]

    return elapsed


def test_time_utils():
    # ensure we add local timezone to time values (in seconds)
    import time

    now = time.time()
    now_str = get_arrow_str_from_time(now)

    # capture client timezone (when job is submitted)
    ctz = get_local_timezone()
    print("\nClient timezone: ", ctz)
    set_local_timezone(ctz)

    # test using local timezone
    now = get_arrow_now_str()
    print("now: {}".format(now))
    dt = parse_time(now)
    print("Parsed time: ", dt)

    # now, test for new york
    ctz = 'US/Eastern'
    print("\nClient timezone: ", ctz)
    set_local_timezone(ctz)

    now = get_arrow_now_str()
    print("now: {}".format(now))

    dt = parse_time(now)
    print("Parsed time: ", dt)

    set_local_timezone(ctz)
    dt = parse_time(now)
    print("Parsed time: ", dt)    

if __name__ == "__main__":
    test_time_utils()