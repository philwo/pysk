#!/usr/bin/env python2

import random

mac = [
    0x02,
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff)
]

print ':'.join(map(lambda x: "%02x" % x, mac))
