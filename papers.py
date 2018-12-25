#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 11:10
import argparse

from easy_tornado.utils.logging import it_print

from core import filter_keys
from core import filter_paper_titles
from data import index


def parse_arguments():
    parser = argparse.ArgumentParser('Papers console')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='show information')

    # function indicator
    exclusive = parser.add_mutually_exclusive_group()
    exclusive.add_argument('-l', '--list-keys', action='store_true', default=False,
                           help='list all keys')
    exclusive.add_argument('-q', '--query', action='store_true', default=False,
                           help='activate query option')

    parser.add_argument('-sk', '--sub-key', help='search all items')

    q = exclusive.add_argument_group('query paper titles')
    q.add_argument('-a', '--all', action='store_true', default=False,
                   help='search all items, if --all is enabled, then --sub-key takes no effect')
    q.add_argument('-s', '--subject', help='partial paper title')

    return parser.parse_known_args()[0]


def list_keys(args):
    version = index.pop('version')
    it_print('version: {}'.format(version))
    it_print('data keys:')
    for _key in filter_keys(index, args.sub_key):
        it_print(_key, indent=2)


def query(args):
    version = index.pop('version')
    it_print('version: {}'.format(version))

    if not args.all:
        filtered = filter_keys(index, args.sub_key)
    else:
        filtered = index.keys()

    paper_titles = []
    for key in filtered:
        part = filter_paper_titles(index[key], args.subject)
        if args.verbose:
            it_print('{:2} => {}'.format(len(part), key))
        paper_titles.extend(part)
    paper_titles = set(paper_titles)

    for i, item in enumerate(paper_titles):
        it_print('{:2}: {}'.format(i + 1, item))


def main(args):
    if args.subject is None:
        args.subject = 'Neural Machine Translation'

    if args.list_keys:
        list_keys(args)
    elif args.query:
        query(args)


if __name__ == '__main__':
    main(parse_arguments())
