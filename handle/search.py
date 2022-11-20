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
from utils.constant import NOT_EXIST, SUCCESS
import os
import socket
from handle.index import Index


class Search(object):

    _data_id_map = {}
    #  更换路径 TODO
    _data_id_map_file = "../py_search_map/1.map"

    def __init__(self):
        """
            初始化数据字典和索引字典
        """
        self.data = Data()
        self.index = Index()
        data_id_map = dump.load_data("../py_search_map/")
        if data_id_map is not None:
            self._data_id_map = data_id_map
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8910))
        if result == 0:
            print("snowflake_start_server is open")
        else:
            os.system("snowflake_start_server")

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

        self.dump_all()

        return data_id

    def dump_all(self):
        """
            将数据字典、索引字典、映射字典持久化
        Returns:

        """
        dump.data_dump(self.data.data_dict, self.data.file_path)
        dump.data_dump(self.index.index_dict, self.index.index_file_path)
        dump.data_dump(self._data_id_map, self._data_id_map_file)

    def search(self, limit=None):
        """
            查询所有记录（默认返回最新插入的10条）
        Returns:

        """
        if limit is None:
            limit = 10
        result = []
        data_keys = list(self.data.data_dict.keys())
        dict_end = len(data_keys) - 1
        for i in range(dict_end, dict_end - limit, -1):
            if i < 0:
                break
            data_id = data_keys[i]
            result.append({data_id: self.data.data_dict[data_id]})
        return result

    def search_index(self):
        return self.index.index_dict

    def search_by_id(self, data_id):
        if data_id in self._data_id_map:
            data_file_path = self._data_id_map[data_id]
            if data_file_path == self.data.file_path:
                return {data_id: self.data.data_dict[data_id]}
        else:
            # TODO 遍历其它映射文件
            pass

    def search_by_key(self, key):
        doc_list = []
        if key in self.index.index_dict:
            index_list = self.index.index_dict[key]
        else:
            # TODO 遍历其它索引文件
            return
        for index in index_list:
            doc_list.append({index[0]: self.data.data_dict[index[0]]})
        return doc_list

    def search_by_key_like(self, key):
        """
            模糊查询 TODO
        Args:
            key:

        Returns:

        """
        pass

    def delete(self, data_id):
        if data_id not in self.data.data_dict:
            # TODO 根据map获取data_id所在的文件，读取文件，再判断是否存在。
            return NOT_EXIST
        data = self.data.data_dict[data_id]
        self.data.data_dict.pop(data_id)
        query = data['query']
        words = analyzer.seg(query)
        self.index.delete(words, data_id)
        self._data_id_map.pop(data_id)
        self.dump_all()

    def modify(self, data_id, answer):
        if data_id not in self.data.data_dict:
            # TODO 根据map获取data_id所在的文件，读取文件，再判断是否存在。
            return NOT_EXIST
        pass
