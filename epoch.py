#!/usr/bin/env python3
import argparse
import datetime
import dateutil.parser
import string
import sys
import time


def parse_arguments():
    """ see http://docs.python.org/library/argparse """
    parser = argparse.ArgumentParser(
        description='Convert string to or from epoch (as appropriate)')
    parser.add_argument('timestr', help='string to convert',
                        nargs='?', default=None)
    parser.add_argument('-b', '--base60time',
                        help='use YYMMDD and base60 time',
                        action="store_true")
    parser.add_argument('-u', '--utc',
                        help='show UTC',
                        action="store_true")
    parser.add_argument('-i', '--integer',
                        help='round off to nearest second',
                        action="store_true")
    return parser.parse_args()


def get_base64_digit(x):
    # some code adapted from http://stackoverflow.com/questions/561486/
    ALPHABET = string.digits + string.ascii_uppercase + \
        string.ascii_lowercase + '-_'
    BASE = len(ALPHABET)
    r = x % BASE
    if x < 0 or x >= BASE:
        raise BaseException(
            str(x) + ' is out of range to represent as single base64 digit')
    return(ALPHABET[r])


def get_base64_time(ttup):
    return get_base64_digit(ttup.tm_hour) + \
        get_base64_digit(ttup.tm_min) + \
        get_base64_digit(ttup.tm_sec)


def epoch_output(timestr, use_base60=False, use_utc=False, intreply=False):
    try:
        # convert timestr into datestr
        epochtime = float(timestr)
        timeobj = datetime.datetime.fromtimestamp(epochtime)
        retval = datetime.datetime.isoformat(timeobj)
    except ValueError:
        # convert timestr into epoch time
        timeobj = dateutil.parser.parse(timestr)
        retval = time.mktime(timeobj.timetuple())
    except TypeError:
        # just print current epoch time
        if(intreply):
            retval = int(time.time())
        else:
            retval = time.time()

    if(use_utc):
        ttup = time.gmtime(retval)
        retval = time.strftime("%Y-%m-%d %H:%M:%S UTC", ttup)

    if(use_base60):
        # we're just going to use UTC for this
        ttup = time.gmtime(retval)
        datepart = time.strftime("%Y%m%d-", ttup)
        retval = datepart + get_base64_time(ttup)

    return retval


def main(argv=None):
    """ Convert string to or from epoch (as appropriate) """

    args = parse_arguments()

    print(epoch_output(args.timestr, use_base60=args.base60time,
                       use_utc=args.utc, intreply=args.integer))


if __name__ == '__main__':
    exit_status = main(sys.argv)
    sys.exit(exit_status)
