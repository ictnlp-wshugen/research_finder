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

data_path = './data'
create_if_not_exists(data_path)

index_path = concat_path(data_path, 'index.json')
dblp_data_path = concat_path(data_path, 'dblp')
create_if_not_exists(dblp_data_path)

if not file_exists(index_path):
    data = {
        'version': 0.1
    }
    write_json_contents(index_path, data)
index = parse_json(load_file_contents(index_path, pieces=False))
