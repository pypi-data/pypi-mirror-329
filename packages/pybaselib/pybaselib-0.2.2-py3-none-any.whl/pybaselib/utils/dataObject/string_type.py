# -*- coding: utf-8 -*-
# @Author: maoyongfan
# @email: maoyongfan@163.com
# @Date: 2025/2/19 19:33

def string_to_bytes_length(string: str) -> int:
    """
    字符串对应字节长度
    :param string:
    :return:
    """
    return len(string.encode('utf-8'))