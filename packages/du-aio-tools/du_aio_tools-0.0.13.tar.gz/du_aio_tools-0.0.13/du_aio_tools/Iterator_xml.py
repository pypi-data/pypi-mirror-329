# -*- coding: utf-8 -*-
# @time: 2024/3/7 15:21
# @author: Dyz
# @file: Iterator_xml.py
# @software: PyCharm
# 读取XML 文件
from pathlib import Path


def iterator_read(file: Path, start: str, encoding='utf-8'):
    """
    迭代器读取
    """
    with open(file, encoding=encoding) as f:
        row_xml = ''
        for line in f:
            # 每条数据的开头
            if line.startswith(start):
                if row_xml:  # 如果有上一条就返回后赋予新的
                    yield row_xml
                    row_xml = line
                    continue
                else:  # 没有上一条就直接加在一起
                    row_xml += line
                    continue
            if row_xml:
                row_xml += line
        if row_xml:
            yield row_xml
