# -*- encoding: utf-8 -*-
"""
@File    :   sys.py
@Time    :   2025/2/25 下午8:22
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


def isMacOS():
        return 'Darwin' in platform.platform()


def shell_run(*args):
        for command in [*args]:
                os.system(f"{command}")


def end():
        exit(0)
        clearDir()


def use_gpu(gpu_id):
        os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_id}"


def get_FileSize(filePath):
    '''获取文件的大小,结果保留两位小数，单位为MB'''
    filePath = unicode(filePath,'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)



'''获取文件的访问时间'''
def get_FileAccessTime(filePath):
    filePath = unicode(filePath,'utf8')
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)


'''获取文件的创建时间'''
def get_FileCreateTime(filePath):
    filePath = unicode(filePath,'utf8')
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


'''获取文件的修改时间'''
def get_FileModifyTime(filePath):
    filePath = unicode(filePath,'utf8')
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)

def merge_txt(data_dir, out_dir, out_name):
    print(f"[run] cat {data_dir}/*.txt > {out_dir}/{out_name}.txt")
    os.system(f"cat {data_dir}/*.txt > {out_dir}/{out_name}.txt")


def merge_file(data_dir, out_dir, out_name, appendix='txt'):
    print(f"[run] cat {data_dir}/* > {out_dir}/{out_name}.{appendix}")
    os.system(f"cat {data_dir}/* > {out_dir}/{out_name}.{appendix}")


def split_file(file_path, split_mode='l', subsize=500, idx_size=4, suffix='txt',output_dir=None):
    split_cmd = "gsplit" if isMacOS() else "split"
    if output_dir is None:
        target_file_dir = os.path.dirname(file_path)
        target_file_name = file_path.split('/')[-1].split('.')[0]
        output_dir = jdir(jpath(target_file_dir, f"{target_file_name}_splits"))
    print(f"[run] {split_cmd} -{split_mode} {subsize} -da {idx_size} {file_path} {output_dir}/data_ --additional-suffix=.{suffix}")
    os.system(f"{split_cmd} -{split_mode} {subsize} -da {idx_size} {file_path} {output_dir}/data_ --additional-suffix=.{suffix}")




