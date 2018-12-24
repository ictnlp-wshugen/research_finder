#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-24 16:01
from __future__ import print_function

import subprocess

base_url = 'https://dblp.org/db/journals/corr/corr{}{:02}.html'

for year in range(2013, 2018 + 1):
    num = year % 100
    for month in range(1, 12 + 1):
        url = base_url.format(num, month)
        cmd = 'python dblp.py -a {}'.format(url)
        print(cmd)
        subprocess.check_call(cmd, shell=True)
        print()
