#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 11:10
import argparse

from easy_tornado.utils.logging import it_print

from data import index


def parse_arguments():
    parser = argparse.ArgumentParser('Papers console')
    parser.add_argument('-l', '--list', action='store_true', help='list data')
    return parser.parse_known_args()[0]


def list_keys():
    version = index.pop('version')
    it_print('version: {}'.format(version))
    it_print('data keys:')
    for key in sorted(index.keys()):
        it_print(key, indent=2)


def main(args):
    if args.list:
        list_keys()


if __name__ == '__main__':
    main(parse_arguments())
