#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 11:10
from easy_tornado.utils.logging import it_print

from data import index


def main():
    version = index.pop('version')
    it_print('version: {}'.format(version))
    it_print('data keys:')
    for key in index:
        it_print(key, indent=2)


if __name__ == '__main__':
    main()
