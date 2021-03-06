#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 09:59
import argparse

from easy_tornado import it_print
from easy_tornado.compat import python3
from easy_tornado.utils import concat_path
from easy_tornado.utils import request
from easy_tornado.utils import to_json
from easy_tornado.utils import write_file_contents
from easy_tornado.utils import write_json_contents

from core import filter_paper_titles
from core import retrieve_paper_titles
from data import dblp_data_path
from data import index
from data import index_path
from data import paper_cache
from data import paper_cache_path


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='url to retrieve data and as key')
    parser.add_argument('-s', '--subject', nargs='+', help='partial paper title')
    parser.add_argument('-r', '--reload', action='store_true', help='reload data from url')

    _args, _ = parser.parse_known_args()
    return _args


def main(args):
    if args.subject is None:
        args.subject = ['Neural Machine Translation']

    key = args.data
    if key not in index or args.reload:
        file_name = key[key.rfind('/') + 1:]
        save_path = concat_path(dblp_data_path, file_name)

        # save data
        contents = request(key)
        if python3 and isinstance(contents, bytes):
            contents = str(contents, encoding='utf-8')
        write_file_contents(save_path, contents)

        # update index
        index[key] = save_path
        index_data = to_json(index, indent=2)
        write_file_contents(index_path, index_data)

        # update cache
        if key not in paper_cache['values']:
            paper_cache['values'][key] = retrieve_paper_titles(index[key], **{
                'source': 'dblp'
            })
        write_json_contents(paper_cache_path, paper_cache)

    filtered, _ = filter_paper_titles(paper_cache['values'][key], args.subject)
    for i, item in enumerate(filtered):
        it_print('{}: {}'.format(i + 1, item))


if __name__ == '__main__':
    main(parse_arguments())
