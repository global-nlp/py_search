# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/15 7:45
# Description: 测试类
# -----------------------------------------------------------------------#
from handle.search import Search


def test_add():
    search = Search()
    data_id = search.add("喜羊羊与灰太狼", "口令正确")
    print("data_id is ", data_id)
    print(search.search())


def test_dump():
    test_add()
    search = Search()
    print(search.search())


def test_index():
    search = Search()
    search.add("敦煌八景之一，被称为沙漠第一泉的是?", "月牙泉")
    print(search.search_index())


def test_search_by_id():
    search = Search()
    data_id = search.add("据说拿破仑阅读了七遍，歌德的第一部小说叫?", "《少年维特之烦恼》")
    print(search.search_by_id(data_id))


def test_delete():
    search = Search()
    data_id = search.add("世界雨极是?", "乞拉朋齐")
    print(search.search())
    print(search.delete(data_id))
    print(search.search())


def test_update_query():
    search = Search()
    search.add("世界雨极是?", "乞拉朋齐")
    print(search.search())
    print(search.update_answer_by_query("世界雨极是?", "布吉岛"))
    print(search.search())


def test_update_data_id():
    search = Search()
    data_id = search.add("世界雨极是?", "乞拉朋齐")
    print(search.search())
    print(search.update_answer_by_data_id(data_id, "布吉岛x2"))
    print(search.search())


def test_batch_add():
    search = Search()
    search.add_from_file("../data/query.txt")
    print(search.search())


if __name__ == '__main__':
    test_add()
    test_dump()
    test_index()
    test_search_by_id()
    test_delete()
    test_update_query()
    test_update_data_id()
    test_batch_add()
