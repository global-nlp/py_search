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
    # data_id = search.add("喜羊羊与灰太狼9", "口令正确")
    # print(data_id)
    print(search.search(2))
    # print(search.search_by_id(4691561912347918337))
    print(search.search_index())
    # print(search.search_by_key("灰太"))
    search.delete(4691909491526991873)
    print("删除后")
    print(search.search(2))
    print(search.search_index())

