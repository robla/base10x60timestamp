Utility to deal with timestamps, including a timestamp format of my
own creation: "base10x60timestamp".

The format:

    YYYYMMDDthms

| Digits | Description  |
|------|-------|
| YYYY | year, base10 digits |
| MM | month, base10 digits |
| DD | date, base10 digits |
| t | timezone ("-" for UTC, which is the only valid choice right now) |
| h | hours, base60 digit (RFC 1924 style) (0-N which is 0-23) |
| m | minutes, base60 digit (0-x, which is 0-59) |
| s | seconds, base60 digit (0-x, which is 0-59) |

Example:

* 20180720-3mf -> 2018-07-20T03:48:41+00:00

Just the time portion from the example:

* 3mf -> 03:48:41

"base60" digit is compatible with the [RFC 1924 base85 format][RFC1924]:

* 0-9: 0-9
* A-Z: 10-35
* a-x: 36-59

This makes the date timestamps sort reasonably on a system supporting lower ascii (UTF-7).  base60 makes the time compact but still marginally readable.

Having "-" represent "UTC" reserves that character in a readable way.  It's possible that future versions might use other characters to represent a timezone offset.

[RFC1924]: https://tools.ietf.org/html/rfc1924

## epoch

epoch is a utility to convert to/from seconds from epoch.

    usage: epoch [-h] [-b] [-u] [-i] [timestr]

    Convert string to or from epoch (as appropriate)

    positional arguments:
      timestr           string to convert

    optional arguments:
      -h, --help        show this help message and exit
      -b, --base60time  use YYMMDD and base60 time
      -u, --utc         show UTC
      -i, --integer     round off to nearest second

epoch is only tangentally related to base60time, because when I started
using base10x60timestamps, this was the utility I added it to.
