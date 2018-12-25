#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 09:59
import argparse

from easy_tornado.utils.file_operation import concat_path
from easy_tornado.utils.file_operation import write_file_contents
from easy_tornado.utils.file_operation import write_json_contents
from easy_tornado.utils.logging import it_print
from easy_tornado.utils.web_extension import request

from core import filter_paper_titles
from data import index, dblp_data_path, index_path


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('data', help='url to retrieve data and as key')
    parser.add_argument('-s', '--subject', help='partial paper title')
    parser.add_argument('-r', '--reload', action='store_true', help='reload data from url')

    _args, _ = parser.parse_known_args()
    return _args


def main(args):
    if args.subject is None:
        args.subject = 'Neural Machine Translation'
    subject = args.subject

    key = args.data
    if key not in index or args.reload:
        file_name = key[key.rfind('/') + 1:]
        save_path = concat_path(dblp_data_path, file_name)

        contents = request(key)
        write_file_contents(save_path, contents)

        index[key] = save_path
        write_json_contents(index_path, index)

    filtered, _ = filter_paper_titles(index[key], subject)
    for i, item in enumerate(filtered):
        it_print('{:2}: {}'.format(i + 1, item))


if __name__ == '__main__':
    main(parse_arguments())
