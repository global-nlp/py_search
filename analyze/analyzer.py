# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/14 13:12
# Description: 用于封装分词相关函数
# -----------------------------------------------------------------------#

from knlp import Knlp


def seg(text):
    """
        Knlp 默认模式分词结果
    Args:
        text: 待分词文本

    Returns: list

    # TODO 如果需要指定不同的分词模式是不是需要引入Segmentor类

    """
    knlp = Knlp(text)
    return knlp.seg_result


if __name__ == "__main__":
    data = {'喜': 1}
    words = seg("喜羊羊与灰太狼")
    for word in words:
        print(data[words[0]])
