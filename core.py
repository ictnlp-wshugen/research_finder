# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-25 15:23
import re

from easy_tornado.utils.file_operation import file_exists, write_json_contents
from easy_tornado.utils.file_operation import load_file_contents
from easy_tornado.utils.str_extension import parse_json
from six import string_types

dblp_regex_fmt = '<li class="entry (?:inproceedings|article|informal)".*?' \
                 '<span class="title" itemprop="name">(.*?).</span>' \
                 '.*?</li>'
dblp_paper_regex = re.compile(dblp_regex_fmt)


def build_paper_titles(paper_cache_path, *data_paths, **kwargs):
    source = kwargs.pop('source', None)
    if source is None or source != 'dblp':
        return
    paper_cache = []
    if file_exists(paper_cache_path):
        paper_cache = parse_json(load_file_contents(paper_cache_path, pieces=False))

    for data_path in data_paths:
        contents = load_file_contents(data_path, pieces=False)
        try:
            contents = contents.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            pass
        paper_titles = dblp_paper_regex.findall(contents)
        paper_cache.extend(paper_titles)
    paper_cache = list(set(paper_cache))
    write_json_contents(paper_cache_path, paper_cache)


def filter_paper_titles(file_path, subject, exclude_subject, logic_and=True):
    if not isinstance(file_path, string_types) or not file_exists(file_path):
        return [], 0

    contents = load_file_contents(file_path, pieces=False)
    try:
        contents = contents.decode('utf-8')
    except UnicodeDecodeError:
        pass

    paper_titles = dblp_paper_regex.findall(contents)
    if subject is None and exclude_subject is None:
        return paper_titles, len(paper_titles)

    filtered = []
    for paper_title in paper_titles:
        y = paper_title.lower()
        if logic_and:
            criterion = all([y.find(x) != -1 for x in subject])
        else:
            criterion = any([y.find(x) != -1 for x in subject])
        if not criterion:
            continue

        if exclude_subject is None or not any([y.find(x) != -1 for x in exclude_subject]):
            filtered.append(paper_title)
    return filtered, len(paper_titles)


def filter_keys(key_holder, sub_key):
    filtered = []
    for _key in sorted(key_holder.keys()):
        if not (sub_key is None or _key.find(sub_key) != -1):
            continue
        filtered.append(_key)
    return filtered
