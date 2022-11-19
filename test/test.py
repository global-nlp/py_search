# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/15 7:45
# Description: 
# -----------------------------------------------------------------------#
from handle.search import Search


if __name__ == '__main__':
    search = Search()
    data_id = search.add("喜羊羊与灰太狼", "口令正确")
    print(data_id)
    print(search.search())
    print(search.search_index())
    # all_data = search.search()
    # print(all_data)
    # for data in all_data:
    #     print(all_data[data])

