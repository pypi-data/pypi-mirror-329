#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = "Copyright (c) 2024 Nuanguang Gu(Sunny) Reserved"
__author__ = "Nuanguang Gu(Sunny)"
__email__ = "nuanguang.gu@aliyun.com"


import time


def get_local_time():
    return time.strftime("%B %d, %y %H:%M:%S", time.localtime())


def get_time_stamp():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())
