# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/19 8:21
# Description: 
# -----------------------------------------------------------------------#
from dump import dump


class Index(object):

    _index_dict = {}
    # TODO 暂时只考虑用一个文件
    _index_file_path = "../py_search_index/1.index"

    def __init__(self):
        """
            从磁盘加载最新的索引文件
        """
        index_dict = dump.load_data("../py_search_index/")
        if index_dict is not None:
            self._index_dict = index_dict

    def insert(self, words, data_id, data_file_path):
        for word in words:
            self.insert_word(word, data_id, data_file_path, False)

    def insert_word(self, word, data_id, data_file_path, is_query=False):
        try:
            doc_list = self._index_dict[word]
            for doc in doc_list:
                if data_id == doc[0]:
                    return
            self._index_dict[word].append((data_id, data_file_path, is_query))
        except Exception as e:
            self._index_dict[word] = [(data_id, data_file_path, is_query)]

    @property
    def index_dict(self):
        return self._index_dict

    @property
    def index_file_path(self):
        return self._index_file_path
