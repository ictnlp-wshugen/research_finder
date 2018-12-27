# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 10:50

from easy_tornado.utils.file_operation import concat_path
from easy_tornado.utils.file_operation import create_if_not_exists
from easy_tornado.utils.file_operation import file_exists
from easy_tornado.utils.file_operation import load_file_contents
from easy_tornado.utils.file_operation import write_json_contents
from easy_tornado.utils.str_extension import parse_json
from six import string_types

from core import build_paper_titles

data_path = './data'
create_if_not_exists(data_path)

cache_path = './cache'
create_if_not_exists(cache_path)

index_path = concat_path(data_path, 'index.json')
paper_cache_path = concat_path(cache_path, 'papers')
query_cache_path = concat_path(cache_path, 'queries')
cache_size = 80

dblp_data_path = concat_path(data_path, 'dblp')
create_if_not_exists(dblp_data_path)

# initialize and load index
if not file_exists(index_path):
    data = {
        'version': 0.1
    }
    write_json_contents(index_path, data)
index = parse_json(load_file_contents(index_path, pieces=False))

# initialize and load paper_cache
if not file_exists(paper_cache_path):
    dblp_data = []
    for key, value in index.items():
        if not isinstance(value, string_types):
            continue
        if value.startswith(dblp_data_path):
            dblp_data.append(value)
    build_paper_titles(paper_cache_path, *dblp_data, **{
        'source': 'dblp'
    })
paper_cache = parse_json(load_file_contents(paper_cache_path, pieces=False))

# initialize and load query_cache
if not file_exists(query_cache_path):
    data = {
        'version': 0.1
    }
    write_json_contents(query_cache_path, data)
query_cache = parse_json(load_file_contents(query_cache_path, pieces=False))
