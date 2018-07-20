#!/usr/bin/env python3

import epoch

for x1 in range(15):
    x2 = x1 + 15
    x3 = x1 + 30
    x4 = x1 + 45
    d1 = epoch.get_base60_digit(x1)
    d2 = epoch.get_base60_digit(x2)
    d3 = epoch.get_base60_digit(x3)
    d4 = epoch.get_base60_digit(x4)
    print("{:>2} {}   {} {}   {} {}   {} {}".format(x1, d1, x2, d2, x3, d3, x4, d4))
    if x1 % 5 == 4:
        print("====")
