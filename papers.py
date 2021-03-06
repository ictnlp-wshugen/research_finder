#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 11:10
import argparse
import sys
from typing import Iterable

from easy_tornado import it_print
from easy_tornado.utils import current_datetime
from easy_tornado.utils import write_json_contents

from core import filter_keys
from core import filter_paper_titles
from data import cache_size
from data import index
from data import paper_cache
from data import query_cache
from data import query_cache_path


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
    exclusive.add_argument('-c', '--cached', action='store_true', default=False,
                           help='list cached keys')

    parser.add_argument('-sk', '--sub-key', help='search all items')

    q = exclusive.add_argument_group('query paper titles')
    q.add_argument('-a', '--all', action='store_true', default=False,
                   help='search all items, if --all is enabled, then --sub-key takes no effect')
    q.add_argument('-s', '--subject', nargs='+', help='partial paper title(s)')
    q.add_argument('-es', '--exclude-subject', nargs='+', help='exclude partial paper title(s)')
    q.add_argument('-m', '--mode', choices=['and', 'or'], default='and',
                   help='criterion logic')
    q.add_argument('-f', '--force', action='store_true', default=False,
                   help='force to query, do not use query_cache')

    c = exclusive.add_argument_group('manipulate query_cache keys')
    c.add_argument('-d', '--delete', help='delete cached item')

    return parser.parse_known_args()[0]


def list_keys(args):
    version = index.pop('version')
    it_print('version: {}'.format(version))
    keys = filter_keys(index, args.sub_key)
    if len(keys) > 0:
        it_print('data keys:')
        for key in keys:
            it_print(key, indent=2)


def cached_query(args):
    c_key = '{sub_key}.{mode}+{subject}-{exclude_subject}'.format(**{
        'sub_key': 'All' if args.all else args.sub_key,
        'mode': args.mode,
        'subject': '/'.join(args.subject) if args.subject is not None else 'All',
        'exclude_subject': '/'.join(args.exclude_subject) if args.exclude_subject is not None else 'None'
    })
    if c_key not in query_cache or args.force:
        if c_key in query_cache:
            last = query_cache[c_key]['time']
        else:
            last = None

        if not args.all:
            filtered = filter_keys(index, args.sub_key)
        else:
            filtered = index.keys()

        paper_titles = []
        total = 0
        cached_paper_titles = paper_cache['values']
        for key in filtered:
            if key not in cached_paper_titles:
                continue
            titles_holder = cached_paper_titles[key]
            part, num = filter_paper_titles(
                titles_holder, args.subject, args.exclude_subject,
                logic_and=args.mode == 'and'
            )
            total += num
            if args.verbose:
                it_print('{:2} => {}'.format(len(part), key))
            if len(part) > 0:
                paper_titles.append({'key': key, 'titles': part})

        # LRU
        c_keys = list(query_cache.keys())
        if len(c_keys) >= cache_size:
            tmp = dict()
            for k, v in query_cache.items():
                if not isinstance(v, Iterable):
                    continue
                if 'time' not in v:
                    continue
                tmp[v['time']] = k
            removed = sorted(tmp.values())[cache_size - 1:]
            for k in removed:
                if k in query_cache:
                    query_cache.pop(k)
        query_cache[c_key] = {
            'paper_titles': paper_titles,
            'total': total,
            'time': current_datetime()
        }
    else:
        v = query_cache[c_key]
        paper_titles, total, last = v['paper_titles'], v['total'], v['time']
        v['time'] = current_datetime()
    write_json_contents(query_cache_path, query_cache)

    if last is not None:
        it_print('last accessed: {}'.format(last))
    it_print('total {} papers'.format(total))
    if not len(paper_titles) > 0:
        it_print('no paper is found')
        return

    it_print('paper search result:')
    for i, item in enumerate(paper_titles, start=1):
        key, titles = item['key'], item['titles']
        it_print('({}) {} -> {}'.format(i, key, len(titles)), indent=2)
        for j, title in enumerate(titles, start=1):
            it_print('{}: {}'.format(j, title), indent=4)
    it_print('total {} papers'.format(total))


def manage_cache(args):
    if args.delete is not None:
        c_key = args.delete
        if c_key in query_cache:
            query_cache.pop(c_key)
            write_json_contents(query_cache_path, query_cache)

    version = query_cache.pop('version')
    it_print('version: {}'.format(version))
    keys = sorted(query_cache.keys())
    if len(keys) > 0:
        it_print('cached keys:')
        for _key in keys:
            it_print(_key, indent=2)


def main(args):
    if args.subject is not None:
        for i, subject in enumerate(args.subject):
            args.subject[i] = subject.lower()
    if args.exclude_subject is not None:
        for i, subject in enumerate(args.exclude_subject):
            args.exclude_subject[i] = subject.lower()
    if args.sub_key is None:
        args.all = True

    if args.list_keys:
        list_keys(args)
    elif args.query:
        cached_query(args)
    elif args.cached:
        manage_cache(args)


if __name__ == '__main__':
    cmd_str = ' '.join(sys.argv[1:])
    if '\'' in cmd_str:
        it_print('please use double quote instead of quote.')
        exit(0)
    main(parse_arguments())
