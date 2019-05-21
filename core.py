# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-25 15:23
import re

from easy_tornado.utils.file_operation import load_file_contents

dblp_regex_fmt = '<li class="entry (?:inproceedings|article|informal)".*?' \
                 '<span class="title" itemprop="name">(.*?).</span>' \
                 '.*?</li>'
dblp_paper_regex = re.compile(dblp_regex_fmt)


def retrieve_paper_titles(data_path, **kwargs):
    source = kwargs.pop('source', None)
    if source is None or source != 'dblp':
        return

    contents = load_file_contents(data_path, pieces=False)
    try:
        contents = contents.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        pass

    return dblp_paper_regex.findall(contents)


def filter_paper_titles(paper_titles, subject=None, exclude_subject=None, logic_and=True):
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
    return filtered, len(filtered)


def filter_keys(key_holder, sub_key):
    filtered = []
    for _key in sorted(key_holder.keys()):
        if sub_key is None or _key.find(sub_key) == -1:
            continue
        filtered.append(_key)
    return filtered
