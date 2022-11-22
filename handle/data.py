# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/19 8:18
# Description: 数据字典处理化及相关函数
# -----------------------------------------------------------------------#
from dump import dump
from utils.constant import PY_SEARCH_PATH


class Data(object):
    _data_dict = {}
    _row = 0
    _file_path = PY_SEARCH_PATH + "data/py_search_data/data.cache"

    def __init__(self):
        data = dump.load_data(self._file_path)
        if data:
            self.data_dict = data

    def insert(self, row, data):
        """
            新增数据记录
        Args:
            row:
            data:

        Returns:

        """
        self.data_dict[row] = data

    @property
    def data_dict(self):
        return self._data_dict

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value

    @property
    def file_path(self):
        return self._file_path

    @data_dict.setter
    def data_dict(self, value):
        self._data_dict = value
