# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-25 15:23
import re

from easy_tornado.utils.file_operation import file_exists
from easy_tornado.utils.file_operation import load_file_contents
from six import string_types


def filter_paper_titles(file_path, subject):
    if not isinstance(file_path, string_types) or not file_exists(file_path):
        return [], 0

    regex_fmt = '<li class="entry (?:inproceedings|article|informal)".*?' \
                '<span class="title" itemprop="name">(.*?).</span>' \
                '.*?</li>'
    paper_entry_regex = re.compile(regex_fmt)
    contents = load_file_contents(file_path, pieces=False)
    try:
        contents = contents.decode('utf-8')
    except UnicodeDecodeError:
        pass

    paper_titles = paper_entry_regex.findall(contents)
    filtered = []
    for paper_title in paper_titles:
        if paper_title.lower().find(subject) != -1:
            filtered.append(paper_title)
    return filtered, len(paper_titles)


def filter_keys(key_holder, sub_key):
    filtered = []
    for _key in sorted(key_holder.keys()):
        if not (sub_key is None or _key.find(sub_key) != -1):
            continue
        filtered.append(_key)
    return filtered
