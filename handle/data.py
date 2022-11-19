# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/19 8:18
# Description: 
# -----------------------------------------------------------------------#
from dump import dump


class Data(object):
    data_dict = {}
    _row = 0
    _file_path = "../py_search_data/1.data"

    def __init__(self):
        data = dump.load_data("../py_search_data/")
        if data is not None:
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
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value

    @property
    def file_path(self):
        return self._file_path
