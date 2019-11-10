# -*- coding: utf-8 -*-
# author: 王树根
# email: wangshugen@ict.ac.cn
# date: 2018-12-20 10:50
from collections import OrderedDict

from easy_tornado import it_print
from easy_tornado.utils import concat_path
from easy_tornado.utils import create_if_not_exists
from easy_tornado.utils import current_datetime
from easy_tornado.utils import file_exists
from easy_tornado.utils import load_file_contents
from easy_tornado.utils import parse_json
from easy_tornado.utils import write_json_contents
from six import string_types

from core import retrieve_paper_titles

data_path = './data'
create_if_not_exists(data_path)

cache_path = './cache'
create_if_not_exists(cache_path)

index_path = concat_path(data_path, 'index.json')
paper_cache_path = concat_path(cache_path, 'papers.json')
query_cache_path = concat_path(cache_path, 'queries.json')
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
index = OrderedDict(index)

# initialize and load paper_cache
if not file_exists(paper_cache_path):
    it_print('building papers cache ...')
    data = {
        'version': 0.1,
        'build_time': current_datetime(),
        'values': {}
    }

    # build cache
    for key, value in index.items():
        if not isinstance(value, string_types):
            continue
        kwargs = {
            'source': None
        }
        if value.startswith(dblp_data_path):
            kwargs['source'] = 'dblp'
        data['values'][key] = retrieve_paper_titles(value, **kwargs)
    write_json_contents(paper_cache_path, data)
paper_cache = parse_json(load_file_contents(paper_cache_path, pieces=False))

# initialize and load query_cache
if not file_exists(query_cache_path):
    data = {
        'version': 0.1
    }
    write_json_contents(query_cache_path, data)
query_cache = parse_json(load_file_contents(query_cache_path, pieces=False))
