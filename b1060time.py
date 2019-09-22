#!/usr/bin/python3
'''
Format: "YYYYMMDD-hms", where the digits YYYYMMDD are simple base10,
  and hms are base60 digits.
Example: "20180726-IEr" > 2018-07-26 18:14:53+00:00

The base60 conversion code was adapted from Miles' answer at
https://stackoverflow.com/a/561704/314034
'''

import argparse
import datetime
import dateutil.parser
import dateutil.tz
import string
import sys
import time


ALPHABET = string.digits + string.ascii_uppercase + \
    string.ascii_lowercase + '-_'
ALPHABET_LOOKUP = dict((c, i) for (i, c) in enumerate(ALPHABET))


def get_base60_digit(x):
    '''
    Convert an integer (0-59) into a base60 digit
    '''
    r = x % 60
    if x < 0 or x >= 60:
        raise BaseException(
            str(x) + ' is out of range to represent as single base60 digit')
    return(ALPHABET[r])


def get_b1060_timestamp_from_epoch(timeval):
    '''
    Convert seconds (from 1970 epoch as float/int) into b1060 timestamp
    '''
    ttup = time.gmtime(timeval)
    datepart = time.strftime("%Y%m%d-", ttup)
    timepart = get_base60_digit(ttup.tm_hour) + \
        get_base60_digit(ttup.tm_min) + \
        get_base60_digit(ttup.tm_sec)
    return datepart + timepart


def parse_b1060_timestamp(ts):
    '''
    Return a datetime object for the given time string

    The string is parsed using dateutil.parser, and will take any
    format that dateutil can handle.
    '''

    year = int(ts[0:4])
    month = int(ts[4:6])
    day = int(ts[6:8])

    hour = ALPHABET_LOOKUP[ts[9]]
    minute = ALPHABET_LOOKUP[ts[10]]
    second = ALPHABET_LOOKUP[ts[11]]

    return datetime.datetime(year, month, day, hour, minute, second, 0, dateutil.tz.UTC)


def main(argv=None):
    """ Convert argument to or from base10x60timestamp """
    parser = argparse.ArgumentParser(
        description='Convert argument to or from base10x60timestamp')
    parser.add_argument('timestr', help='time to convert',
                        nargs='?', default=None)
    args = parser.parse_args()

    try:
        # first see if the string is something like "20180726-IEr"
        print(parse_b1060_timestamp(args.timestr))
    except ValueError:
        # now see if we have a time string that dateutil can parse
        timeobj = dateutil.parser.parse(args.timestr)
        print(get_b1060_timestamp_from_epoch(timeobj.timestamp()))
    except TypeError:
        # fine...it's probably an empty value.  we'll just assume that
        # the user just wants a b1060 timestamp for the current time
        retval = time.time()
        print(get_b1060_timestamp_from_epoch(retval))


if __name__ == '__main__':
    exit_status = main(sys.argv)
    sys.exit(exit_status)
