# -*- encoding: utf-8 -*-
"""
@File    :   algo.py
@Time    :   2025/2/25 下午8:31
@Author  :   Li Jiawei
@Version :   1.0
@Contact :   Li.J.W.adrian421@hotmail.com
@License :   (C)Copyright 2023-2030
@Desc    :   None
@Brief   :
"""
import os, sys, argparse
from tqdm import tqdm
from itertools import groupby, tee
from datetime import timedelta
from collections import Counter
import codecs, json, \
        time, datetime, pickle, \
        re, random, numpy as np, \
        pandas as pd, xml.dom.minidom as xmldom, string
import inspect
import platform
import yaml
import itertools
from pdb import set_trace as stop
from typing import Any, List, Tuple, Union


def dupstr(source, elmt):  # The source may be a list or string.
        elmt_index = []
        s_index = 0
        e_index = len(source)
        while s_index < e_index:
                try:
                        temp = source.index(elmt, s_index, e_index)
                        elmt_index.append(temp)
                        s_index = temp + 1
                except ValueError:
                        break
        return elmt_index


def retgroup(inputlst):
        ''' 返回连续序列中的连续相同项 '''
        groups = [(k, sum(1 for _ in g)) for k, g in groupby(inputlst)]
        cursor = 0
        result = []
        for k, l in groups:
                result.append((k, [cursor, cursor + l - 1]))
                cursor += l
        return result


def find_substr_all(in_string, substr):
        """
        找到不重叠的子串的位置
        :param in_string:
        :param substr:
        :return:
        """
        out_pos = []
        if not in_string or not substr:
                return []
        start = 0
        is_found = in_string[start:].find(substr)
        while is_found != -1:
                assert in_string[start + is_found:start + is_found + len(substr)] == substr
                out_pos.append((start + is_found, start + is_found + len(substr)))
                start = start + is_found + len(substr)
                is_found = in_string[start:].find(substr)
        return out_pos


def argmin(lst):
        return min(range(len(lst)), key=lst.__getitem__)


def argmax(lst):
        return max(range(len(lst)), key=lst.__getitem__)


def groupby_continuous_index(index_list):
        from itertools import groupby
        func = lambda x: x[1] - x[0]
        output = []
        for k, g in groupby(enumerate(index_list), func):
                l1 = [j for i, j in g]  # 连续数字的列表
                if len(l1) > 1:
                        scop = list(range(min(l1), max(l1) + 1))  # 将连续数字范围用"-"连接
                else:
                        scop = l1[0]
                output.append(scop)
        return output


# NLP

def punctuation_split(txt):
        pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
        return re.split(pattern, txt)


def strip_margin(text):
        return re.sub('\n[ \t]*\|', '\n', text)


def strip_heredoc(text):
        indent = len(min(re.findall('\n[ \t]*(?=\S)', text) or ['']))
        pattern = r'\n[ \t]{%d}' % (indent - 1)
        return re.sub(pattern, '\n', text)


def getRidOfPunc(inputs):
        """
        [usage]: 去除文本中的标点符号，只提取中文英文数字
        """
        cn_text = re.compile(r'[\u4e00-\u9fa5_a-zA-Z0-9]{2,50}', re.IGNORECASE)
        tokens = cn_text.findall(inputs)
        return ''.join(tokens)


def getZhChar(inputs):
        """
        [usage]: 只提取中文
        """
        cn_text = re.compile(r'[\u4e00-\u9fa5]{1,50}', re.IGNORECASE)
        tokens = cn_text.findall(inputs)
        return ''.join(tokens)


def getEnChar(inputs):
        """
        [usage]: 只提取英文
        """
        cn_text = re.compile(r'[a-zA-Z]{1,50}', re.IGNORECASE)
        tokens = cn_text.findall(inputs)
        return ''.join(tokens)


def getNumChar(inputs):
        """
        [usage]: 只提取数字
        """
        cn_text = re.compile(r'[0-9]{1,50}', re.IGNORECASE)
        tokens = cn_text.findall(inputs)
        return ''.join(tokens)


def extract_room_expr(inputs):
    """
    [usage]: 提取XXX室（门牌号表达）
    """
    room_rg = re.compile("[a-zA-Z0-9\-甲乙丙丁戊己庚戌东南西北一二三四五六七八九]+室", re.IGNORECASE)
    expr_list = room_rg.findall(inputs)
    return expr_list




