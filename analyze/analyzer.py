# !/usr/bin/python
# -*- coding:UTF-8 -*-
# -----------------------------------------------------------------------#
# Author: Feng Qing Liu
# Mail: liu_f_q@163.com
# Created Time: 2022/11/14 13:12
# Description: 分词相关函数
# -----------------------------------------------------------------------#

from knlp import Knlp


def seg(text):
    """
        调用Knlp默认分词模式进行分词
    Args:
        text: 待分词文本

    Returns: 分词结果 list
    """

    knlp = Knlp(text)
    return knlp.seg_result


if __name__ == "__main__":
    words = seg("喜羊羊与灰太狼")
    print(words)
