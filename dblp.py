#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 09:59
import argparse
import re

from easy_tornado.utils.file_operation import load_file_contents
from easy_tornado.utils.logging import it_print
from easy_tornado.utils.web_extension import request


def parse_arguments():
    parser = argparse.ArgumentParser('DBLP Papers Helper')
    parser.add_argument('--debug', action='store_true', help='whether or not a debug mode')
    parser.add_argument('--subject', '-s', help='partial paper title')
    parser.add_argument('--url', '-a', required=True, help='html address')

    _args, _ = parser.parse_known_args()
    return _args


def main(args):
    regex_fmt = '<li class="entry inproceedings".*?<span class="title" itemprop="name">(.*?).</span>.*?</li>'
    paper_entry_regex = re.compile(regex_fmt)

    if args.subject is None:
        subject = 'Neural Machine Translation'
    else:
        subject = args.subject

    if args.debug:
        contents = load_file_contents(args.url, pieces=False)
    else:
        url = args.url
        contents = request(url)
    contents = contents.decode('utf-8')

    paper_titles = paper_entry_regex.findall(contents)
    filtered = []
    for paper_entry in paper_titles:
        try:
            if paper_entry.index(subject):
                filtered.append(paper_entry)
        except ValueError:
            continue

    for i, item in enumerate(filtered):
        it_print('{:2}: {}'.format(i + 1, item))


if __name__ == '__main__':
    main(parse_arguments())
