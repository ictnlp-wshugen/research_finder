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
    parser.add_argument('-k', '--key', help='key item')
    return parser.parse_known_args()[0]


def list_keys(key=None):
    version = index.pop('version')
    it_print('version: {}'.format(version))
    it_print('data keys:')
    for _key in sorted(index.keys()):
        if not (key is None or _key.find(key) != -1):
            continue
        it_print(_key, indent=2)


def main(args):
    if args.list:
        list_keys(args.key)


if __name__ == '__main__':
    main(parse_arguments())
