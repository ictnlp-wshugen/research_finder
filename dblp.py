#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 09:59
import argparse
import re

from easy_tornado.utils.file_operation import load_file_contents, write_file_contents, concat_path, write_json_contents
from easy_tornado.utils.logging import it_print
from easy_tornado.utils.web_extension import request

from data import index, dblp_data_path, index_path


def parse_arguments():
    parser = argparse.ArgumentParser('DBLP Papers Helper')
    parser.add_argument('--subject', '-s', help='partial paper title')
    parser.add_argument('--url', '-a', required=True, help='html address')
    parser.add_argument('--reload', action='store_true', help='reload data from url')

    _args, _ = parser.parse_known_args()
    return _args


def main(args):
    regex_fmt = '<li class="entry inproceedings".*?<span class="title" itemprop="name">(.*?).</span>.*?</li>'
    paper_entry_regex = re.compile(regex_fmt)

    if args.subject is None:
        subject = 'Neural Machine Translation'
    else:
        subject = args.subject

    key = args.url
    if key not in index or args.reload:
        file_name = key[key.rfind('/') + 1:]
        save_path = concat_path(dblp_data_path, file_name)

        contents = request(args.url)
        write_file_contents(save_path, contents)

        index[key] = save_path
        write_json_contents(index_path, index)
    contents = load_file_contents(index[args.url], pieces=False)
    contents = contents.decode('utf-8')

    paper_titles = paper_entry_regex.findall(contents)
    filtered = []
    for paper_title in paper_titles:
        if paper_title.find(subject) != -1:
            filtered.append(paper_title)

    for i, item in enumerate(filtered):
        it_print('{:2}: {}'.format(i + 1, item))


if __name__ == '__main__':
    main(parse_arguments())
