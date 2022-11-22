# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/19 8:21
# Description: 索引字典初始化及相关函数
# -----------------------------------------------------------------------#
import os
from utils.constant import NOT_EXIST, PY_SEARCH_PATH
from dump import dump


class Index(object):

    _index_dict = {}
    _index_dir = PY_SEARCH_PATH + "data/py_search_index/"
    _index_file_path = PY_SEARCH_PATH + "data/py_search_index/index.cache"

    def __init__(self):
        """
            从磁盘加载最新的索引文件
        """
        index_dict = dump.load_data(self.index_file_path)
        if index_dict:
            self._index_dict = index_dict

    def insert(self, words, data_id, data_file_path):
        for word in words:
            self.insert_word(word, data_id, data_file_path, False)

    def insert_word(self, word, data_id, data_file_path, is_query=False):
        """
            插入单个词
        Args:
            word: 关键词
            data_id:
            data_file_path:
            is_query: 关键词是否为问题本身

        Returns:

        """
        if word in self._index_dict:
            for doc in self._index_dict[word]:
                if data_id == doc[0]:
                    return
                self._index_dict[word].append((data_id, data_file_path, is_query))

        # 当前索引没有, 遍历所有索引字典
        for file_name in os.listdir(self._index_dir):
            if os.path.basename(file_name).__contains__(".cache"):
                continue
            temp_index_dict = dump.load_data(self._index_dir + file_name)
            if word not in temp_index_dict:
                continue
            # 在某个索引字典中找到关键词, 判断是否文档是否已经存在
            for doc in self._index_dict[word]:
                if data_id == doc[0]:
                    return
            self._index_dict[word].append((data_id, data_file_path, is_query))
            return

        # 所有索引字典都没有
        self._index_dict[word] = [(data_id, data_file_path, is_query)]

    def get_doc_list_by_word(self, word):
        """
            遍历非当前索引字典，获取关键词对应的文档list
        Returns:

        """
        for file_name in os.listdir(self._index_dir):
            temp_index_dict = dump.load_data(self._index_dir + file_name)
            if word in temp_index_dict:
                return temp_index_dict[word]
        return []

    def delete(self, words, data_id):
        """
            删除多个关键词
        Args:
            words: 关键词list
            data_id: data_id

        Returns:

        """
        for word in words:
            self.delete_word(word, data_id)

    def delete_word(self, word, data_id):
        """
            删除单个关键词
        Args:
            word: 关键词
            data_id: data_id

        Returns:

        """
        if word in self.index_dict:
            self.delete_word_from_index_dict(data_id, word)
            dump.data_dump(self.index_dict, self.index_file_path)
            return
        # 当前索引字典中没有, 遍历其它索引文件
        for file_name in os.listdir(self._index_dir):
            temp_index_dict = dump.load_data(self._index_dir + file_name)
            if word in temp_index_dict:
                self.delete_word_from_index_dict(data_id, word)
                dump.data_dump(temp_index_dict, self._index_dir + file_name)
                return

        # 没有找到该关键词
        return NOT_EXIST

    def delete_word_from_index_dict(self, data_id, word):
        doc_index_list = self.index_dict[word]
        if len(doc_index_list) == 1:
            # 该关键词只对应一个文档, 直接删除该关键词
            self.index_dict.pop(word)
            return
        for doc_index in doc_index_list:
            if doc_index[0] == data_id:
                doc_index_list.remove(doc_index)
        return

    @property
    def index_dict(self):
        return self._index_dict

    @property
    def index_file_path(self):
        return self._index_file_path

    def get_index_dict_by_key(self, query):
        """
            根据关键词(问题)查找对应的索引字典
        Args:
            query: 关键词(问题)

        Returns: 索引字典, 字典文件路径

        """
        for file in os.listdir(self._index_dir):
            index_dict = dump.load_data(self._index_dir + file)
            if query in index_dict:
                return index_dict
        return {}
