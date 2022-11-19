# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/19 9:57
# Description: 
# -----------------------------------------------------------------------#
import os


def to_study():
    # TODO 不理解，为什么捕获了还会打印异常信息
    try:
        os.system("snowflake_start_server")
    except Exception as e:
        print(e)
    print("1")
    # try:
    #     print(1/0)
    # except Exception as e:
    #     print(e)


if __name__ == '__main__':
    # to_study()

    data = {}
    record = []
    record.append((1, 2))
    data['1'] = record
    print(data['1'])
    data['1'].append((3, 4))
    print(data['1'])
