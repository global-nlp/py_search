# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/19 9:57
# Description: 
# -----------------------------------------------------------------------#
import socket


if __name__ == '__main__':
    # data = {"1": 1, '123': 123, "asd": 111, "122": 121}
    data = [(1, 2), (3, 4)]
    for d in data:
        if d[0] == 1:
            print("==")
            data.pop(d)
    print(data)
