# -*- encoding: utf-8 -*-
"""
@File    :   ops.py
@Time    :   2025/2/25 下午8:23
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
from algo import groupby_continuous_index


def clearDir(*args):
        os.system("""find . -name "__pycache__"|xargs rm -rf""")
        os.system("""find . -name ".DS_Store"|xargs rm -rf""")
        for pattern in [*args]:
                os.system(f"""find . -name "{pattern}"|xargs rm -rf""")


def jdir(dirpath):
        os.makedirs(dirpath, exist_ok=True)
        return dirpath


def jpath(*args):
        full_path = os.path.join(*args)
        dirs = full_path.split('/')[:-1] if '/' in full_path else (full_path.split('\\')[:-1] if '\\' in full_path else '')
        dirs = [x for x in dirs if x]
        if dirs:
                for i in range(len(dirs)):
                        dir_path = jdir('/' + '/'.join(dirs[:i + 1]))
        return full_path


def say(txt):
        print(f"『 {txt} 』")
        return f"『 {txt} 』"


def show_rows(row):
        for idx, item in enumerate(row):
                print(f"[{idx}] {item}")


def db(expression, showValue=True, showUnique=False):
        '''
        :param expression: format: 'variable' or "variable"
        :param showValue: bool,whether show variable's content, if False, simply show the type and shape
        :return: None
        '''
        frame = sys._getframe(1)
        var = eval(expression, frame.f_globals, frame.f_locals)
        print('\n')
        print('-' * 25)
        print('[NAME] : %s' % expression)
        print("[TYPE] :", type(var))
        try:
                print("[SHAPE]:", var.shape)
                try:
                        var1 = var.flatten()
                        print(f"[STAT]: mean = {np.mean(var1):.4f}, min = {np.min(var1):.4f}, max = {np.max(var1):.4f}, median = {np.median(var1):.4f}, std={np.std(var1):.4f}, unique_num = {len(list(set(var1.tolist())))}")
                        if showUnique:
                                print(f"[UNIQUE VAL]: {list(set(var1.tolist()))}")
                except:
                        pass
        except:
                pass
        try:
                print("[LEN] :", len(var))
                try:
                        print(f"[STAT]: mean = {np.mean(var):.4f}, min = {np.min(var):.4f}, max = {np.max(var):.4f}, median = {np.median(var):.4f}, std={np.std(var):.4f}, unique_num = {len(list(set(var)))}")
                        if showUnique:
                                print(f"[UNIQUE VAL]: {list(set(var1))}")
                except:
                        pass
        except:
                pass
        if showValue:
                print('[VALUE]:', repr(var))
        if isinstance(eval(expression, frame.f_globals, frame.f_locals), dict):
                print('[KEYS] :', list(var.keys()))
        print('-' * 25)


def current_method_name():
        '''获取正在运行函数(或方法)名称'''
        return inspect.stack()[1][3]


def testbug(code, var):
        try:
                exec(code)
        except:
                raise ValueError(f"[CODE] try executing「{code}」 Failed! var is {var}")


def pairwise(it):
        """
        获取元素间的顺序对

        Parameter:
        ----------
        it: 列表或者迭代器，例如(s0,s1,s2,...,sn)

        Return:
        -------
        pair: (s0,s1),(s1,s2),(s2, s3),...,(sn-1, sn)
        """
        a, b = tee(it)
        next(b, None)
        return zip(a, b)


def inverse_dict(my_dict):
        """
        Get the key and values swapped new dict from an old dict

        Parameter:
        ----------
        my_dict: dict, {k:v}

        Return:
        -------
        {v:k}
        """
        return {v: k for k, v in my_dict.items()}


def flatten_multi_list(lst):
        return list(itertools.chain.from_iterable(lst))


def tqdmenum(x, desc):
        return tqdm(enumerate(x), total=len(x), desc=f"{desc}")


def mapfn(lambda_expression, lst):
        return list(map(lambda_expression, lst))


def fold_list(lst):
        """
        example:
        inputs:
                 [1, 2, 1, 2, 1, 2, 3, 4, 4, 4, 5, 6, 6, 7, 6, 7, 9, 9, 9, 9, 1, 2, 3, 4]
        outputs:
                 [1, 2, 1, 2, 1, 2, 3, '4>r3', 5, '6>r2', 7, 6, 7, '9>r4', 1, 2, 3, 4]

        """
        lst = lst + [-999314525]  # magic number, used to avoid that our function misses the last token of lst
        label_lst = ['0']
        for idx in range(1, len(lst)):
                label = '1' if lst[idx - 1] == lst[idx] else '0'
                label_lst.append(label)
        outputs = []
        for group in return_group(label_lst):
                if group[0] == '1':
                        outputs.append('>r'.join([str(lst[group[1][0] - 1]), str(group[1][1] - group[1][0] + 2)]))
                if group[0] == '0':
                        outputs.extend(lst[group[1][0]:group[1][1]])
        return outputs


def unfold_list(lst):
        """
        example:
        inputs:
                [1, 2, 1, 2, 1, 2, 3, '4>r3', 5, '6>r2', 7, 6, 7, '9>r4', 1, 2, 3, 4]
        outputs:
                [1, 2, 1, 2, 1, 2, 3, 4, 4, 4, 5, 6, 6, 7, 6, 7, 9, 9, 9, 9, 1, 2, 3, 4]

        """
        outputs = []
        for item in lst:
                if isinstance(item, str) and '>r' in item:
                        outputs += [param_to_number(item.split('>r')[0])] * param_to_number(item.split('>r')[1])
                else:
                        outputs += [param_to_number(item)]
        return outputs


def simplyfy_list(lst):
        lst = groupby_continuous_index(lst)
        lst = fold_list(lst)
        outputs = []
        for item in lst:
                if isinstance(item, list) and not '>r' in item:
                        outputs += [f"{item[0]}>c{len(item)}"]
                else:
                        outputs += [item]
        return outputs


def recover_list(lst):
        """
        example:
            inputs:
                [1, 2, 1, 2, 1, 2, 3, 4, 4, 4, 4, 3, 2, 5, 6, 6, 7, 6, 7, 9, 9, 9, 9, 1, 2, 3, 4]
                ['1>c2', '1>c2', '1>c4', '4>r3', 3, 2, '5>c2', '6>c2', '6>c2', '9>r4', '1>c4']
            outputs:
                [1, 2, 1, 2, 1, 2, 3, 4, 4, 4, 4, 3, 2, 5, 6, 6, 7, 6, 7, 9, 9, 9, 9, 1, 2, 3, 4]
        """
        outputs = []
        for item in lst:
                if isinstance(item, str):
                        if '>c' in item:
                                outputs += [int(item.split('>c')[0]) + i for i in range(int(item.split('>c')[1]))]
                                continue
                        if '>r' in item:
                                outputs += [param_to_number(item.split('>r')[0])] * param_to_number(item.split('>r')[1])
                                continue
                        else:
                                outputs += [item]
                                continue
                else:
                        outputs += [item]
        return outputs


def rows2cols(rows):
        """
        Convert rows like [[1,2,3],[4,5,6]] into columns like
        [[1,4],[2,5],[3,6]]

        Parameter:
        ----------
        rows: list, forms like [[1,2,3],[4,5,6]]

        Return:
        -------
        List like [[1,4],[2,5],[3,6]]
        """
        return list(zip(*rows))


def param_is_number(s):
        try:
                int(s)
                return True
        except ValueError:
                pass
        try:
                float(s)
                return True
        except (TypeError, ValueError):
                pass
        return False


def param_to_number(s):
        try:
                return int(s)
        except ValueError:
                pass
        try:
                return float(s)
        except (TypeError, ValueError):
                pass
        return s


def find_declared(fpath, declaration_name):
        ''' customize declaration field

        example:

            cfg.py:

                def useful():
                    def decorator(fn):
                        return fn
                    return lambda fn: decorator(fn)

                由于python中@只用于函数装饰器，因此若要修饰变量，只能将变量函数化
                class Params(object):
                    def __init__(self):
                        self.name('Alex')
                        self.age(23)
                        self.score(100)
                    def name(self,name):
                        self.name = name
                    @useful
                    def age(self,age):
                        self.age = age
                    @useful
                    def score(self,score):
                        self.score = score

            main.py:

                def get_useful_param():
                    fields = find_declared("cfg.py","@useful")
        '''
        fields = []
        with open(fpath, 'r', encoding='utf-8') as f:
                line = f.readline()
                while line:
                        line = line.strip()
                        if line.startswith(f"{declaration_name}"):
                                line = f.readline()
                                target = re.findall('\s(.*?)\(', line)[0]
                                fields.append(target.strip())
                        line = f.readline()
                return fields
