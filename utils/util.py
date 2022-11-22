# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/21 12:30
# Description: 工具方法
# -----------------------------------------------------------------------#
import os
import socket
import time


def open_snowflake_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8910))
    if result == 0:
        print("snowflake_start_server is open")
    else:
        os.system("snowflake_start_server")
        time.sleep(1)
