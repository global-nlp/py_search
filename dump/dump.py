# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/19 7:44
# Description: 持久化数据以及索引
# -----------------------------------------------------------------------#
import pickle
import os


def data_dump(data_dict, path):
    """
        将数据记录字典持久化
    Args:
        data_dict: 数据记录对应的字典
        path: 持久化的目标文件路径名

    Returns:

    """
    data_file = open(path, "wb")
    pickle.dump(data_dict, data_file)
    data_file.close()


def load_data(path=None):
    """
        加载数据文件
    Args:
        path: 指定数据文件路径。path为None时，加载最新的文件

    Returns: 数据字典

    """
    # 获取当前路径下所有文件，遍历 获取最新的文件
    file_list = os.listdir(path)
    file_name = max(file_list, key=lambda file: os.path.getmtime(path + file))
    if "__init__.py".__eq__(file_name):
        return None
    else:
        data_file_path = path + file_name
        data_file = open(data_file_path, "rb")
        data = pickle.load(data_file)
        data_file.close()
        return data


def load_index(path=None):
    """
        加载倒排索引字典
    Args:
        path: 指定索引文件路径。path为None时，加载最新的文件

    Returns:

    """
    # TODO
    pass
