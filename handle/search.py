# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/16 8:12
# Description: 数据增删改查核心处理逻辑
# -----------------------------------------------------------------------#
from analyze import analyzer
from dump import dump
from handle.data import Data
import snowflake.client as snow
from utils.constant import NOT_EXIST, SUCCESS, PY_SEARCH_PATH
from utils.util import open_snowflake_server
import threading
from handle.index import Index


class Search(object):

    _data_id_map = {}
    _data_id_map_file = PY_SEARCH_PATH + "data/py_search_map/map.cache"

    def __init__(self):
        """
            初始化数据字典和索引字典
        """
        self.data = Data()
        self.index = Index()
        data_id_map = dump.load_data(self._data_id_map_file)
        if data_id_map:
            self._data_id_map = data_id_map

    def head(self, data_id):
        """
            查询根据id查询数据是否存在
        Args:
            data_id: data_id

        Returns:

        """
        return self.search_by_id(data_id)

    def add(self, query, answer):
        """
            问答对新增保存
        Args:
            query: 问题 (目前仅对问题分词)
            answer: 答案

        Returns: 新增数据的id

        """
        thread = threading.Thread(target=open_snowflake_server)
        thread.start()
        # 数据插入
        data_id = snow.get_guid()
        return self.add_with_data_id(data_id, query, answer)

    def add_with_data_id(self, data_id, query, answer):
        """
            问答对新增保存
        Args:
            data_id: 添加时指定id
            query: 问题 (目前仅对问题分词)
            answer: 答案

        Returns: 新增数据的id

        """
        record = {'query': query, 'answer': answer}
        self.data.insert(str(data_id), record)

        # 数据id关联数据所在文件
        self._data_id_map[data_id] = self.data.file_path.replace(".cache", "")
        words = analyzer.seg(query)
        self.index.insert(words, data_id, self.data.file_path)
        self.index.insert_word(query, data_id, self.data.file_path, True)

        self.dump_all_cache()

        return data_id

    def add_from_file(self, query_file_path):
        """
            从文件中读取问答对，批量添加
        Args:
            query_file_path:

        Returns:

        """

        file = open(query_file_path, "r", encoding="utf-8")
        while 1:
            lines = file.readlines(1000)
            if not lines:
                break
            for line in lines:
                query, answer = line.split("//")
                self.add(query, answer)

    def dump_all_cache(self, dump_data=True, dump_index=True, dump_map=True):
        """
            将数据字典、索引字典、映射字典持久化
        Returns:

        """
        if dump_data:
            dump.data_dump(self.data.data_dict, self.data.file_path)
        if dump_index:
            dump.data_dump(self.index.index_dict, self.index.index_file_path)
        if dump_map:
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
        # 从后往前取10条
        for i in range(dict_end, dict_end - limit, -1):
            if i < 0:
                break
            data_id = data_keys[i]
            result.append({data_id: self.data.data_dict[data_id]})
        return result

    def search_index(self):
        return self.index.index_dict

    def search_by_id(self, data_id):
        """
            根据id查询记录
        Args:
            data_id:

        Returns: {data_id: data}

        """
        if data_id in self.data.data_dict:
            return {data_id: self.data.data_dict[data_id]}
        if data_id in self._data_id_map:
            data_file_path = self._data_id_map[data_id]
            # 加载指定数据文件
            data_dict_tmp = dump.load_data(data_file_path)
            if not data_dict_tmp:
                return NOT_EXIST
            if data_id in data_dict_tmp:
                return {data_id: data_dict_tmp[data_id]}
        # TODO 暂时只考虑一个映射文件
        return NOT_EXIST

    def search_by_key(self, key):
        """
            关键关键词查询对应的文档list (精确查找)
        Args:
            key:

        Returns: 数据字典 {data_id: data_dict[data_id]}

        """
        doc_list = []
        if key in self.index.index_dict:
            index_list = self.index.index_dict[key]
        else:
            index_list = self.index.get_doc_list_by_word(key)
        if len(index_list) == 0:
            # 所有索引文件中都没有
            return NOT_EXIST
        for index in index_list:
            # 遍历关键词对应的索引list，根据data_id获取对应的数据记录
            if index[0] in self.data.data_dict:
                doc_list.append({index[0]: self.data.data_dict[index[0]]})
            else:
                data_list_tmp = self.search_by_id(index[0])
                if NOT_EXIST.__eq__(data_list_tmp):
                    continue
                doc_list.append({index[0]: data_list_tmp[index[0]]})
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
        """
            根据数据id删除数据及对应的关键词索引
        Args:
            data_id:

        Returns:

        """
        if data_id in self.data.data_dict:
            self.delete_from_other_file(data_id, self.data.data_dict, self._data_id_map)
            # 删除索引的方法中已经实现了索引字典的持久化
            self.dump_all_cache(dump_index=False)
            return SUCCESS

        if data_id in self._data_id_map:
            # 在其它数据文件中
            data_file_path = self._data_id_map[data_id]
            data_dict_tmp = dump.load_data(data_file_path)
            if not data_dict_tmp:
                return NOT_EXIST
            self.delete_from_other_file(data_id, data_dict_tmp, self._data_id_map)
            # 没有操作cache数据字典, 不进行持久化
            self.dump_all_cache(dump_data=False, dump_index=False)
            dump.data_dump(data_dict_tmp, data_file_path)
            return SUCCESS
        return NOT_EXIST

    def delete_from_other_file(self, data_id, data_dict, data_id_map):
        """
            从非cache字典中删除数据
        Args:
            data_id:
            data_dict:
            data_id_map: 数据id与存放文件的映射字典

        Returns:

        """
        data = data_dict[data_id]
        data_dict.pop(data_id)
        query = data['query']
        words = analyzer.seg(query)
        self.index.delete(words, data_id)
        data_id_map.pop(data_id)

    def update_answer_by_data_id(self, data_id, answer):
        """
            根据数据id修改问题答案
        Args:
            data_id:
            answer: data_id这条数剧的答案

        Returns:

        """
        if data_id in self.data.data_dict:
            self.data.data_dict[data_id]['answer'] = answer
            self.dump_all_cache(dump_index=False, dump_map=False)

        if data_id in self._data_id_map:
            # 数据在其它数据字典中
            data_file_path = self._data_id_map[data_id]
            data_dict = dump.load_data(data_file_path)
            if not data_dict:
                return NOT_EXIST
            data_dict[data_id]['answer'] = answer
            dump.data_dump(data_dict, data_file_path)
        return NOT_EXIST

    def update_answer_by_query(self, query, answer):
        """
            根据问题修改答案
        Args:
            query: 待修改的问题
            answer: 问题的答案

        Returns:

        """
        # 找到关键词所在的索引字典及文件路径
        if query in self.index.index_dict:
            index_dict = self.index.index_dict
        else:
            index_dict = self.index.get_index_dict_by_key(query)

        if len(index_dict) > 0:
            doc_index_list = index_dict[query]
            # 一个问题可以存在多个答案
            for doc_index in doc_index_list:
                data_id = doc_index[0]
                self.update_answer_by_data_id(data_id, answer)
