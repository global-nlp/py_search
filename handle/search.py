# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/16 8:12
# Description: 
# -----------------------------------------------------------------------#
from analyze import analyzer
from dump import dump
from handle.data import Data
import snowflake.client as snow
import os

# TODO 什么时候需要使用类，方法被调用之前需要先初始化一些变量的时候？
from handle.index import Index


class Search(object):

    _data_id_map = {}
    _data_id_map_file = "../py_search_map/1.map"

    def __init__(self):
        self.data = Data()
        self.index = Index()
        data_id_map = dump.load_data("../py_search_map/")
        if data_id_map is not None:
            self._data_id_map = data_id_map
        try:
            os.system("snowflake_start_server")
        except Exception as e:
            print(e.__cause__)
        """
            初始化数据字典和索引字典
        """
        # TODO

    def add(self, query, answer):
        """
            问答对新增保存
        Args:
            query: 问题 (目前仅对问题分词)
            answer: 答案

        Returns: 新增数据的id

        """
        # 数据插入
        data_id = snow.get_guid()
        record = {'query': query, 'answer': answer}
        self.data.insert(data_id, record)

        # 索引插入
        data_file_path = self.data.file_path
        self._data_id_map[data_id] = data_file_path
        words = analyzer.seg(query)
        self.index.insert(words, data_id, self.data.file_path)
        self.index.insert_word(query, data_id, self.data.file_path, True)

        # 持久化
        dump.data_dump(self.data.data_dict, data_file_path)
        dump.data_dump(self.index.index_dict, self.index.index_file_path)
        dump.data_dump(self._data_id_map, self._data_id_map_file)

        return data_id

    def modify(self):
        # TODO
        pass

    def delete(self):
        # TODO
        pass

    def search(self):
        """
            查询所有记录
        Returns:

        """

        return self.data.data_dict

    def search_index(self):
        return self.index.index_dict
