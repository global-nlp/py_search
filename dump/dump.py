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


def load_data(path):
    """
        加载指定文件
    Args:
        path: 指定文件路径

    Returns: 字典

    """
    if not os.path.exists(path):
        return {}
    data_file = open(path, "rb")
    data = pickle.load(data_file)
    data_file.close()
    return data
