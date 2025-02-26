# -*- encoding: utf-8 -*-
"""
@File    :   logger.py
@Time    :   2025/2/25 下午8:46
@Author  :   Li Jiawei
@Version :   1.0
@Contact :   Li.J.W.adrian421@hotmail.com
@License :   (C)Copyright 2023-2030
@Desc    :   None
@Brief   :
"""

# here put the import lib
import os,sys,argparse,logging
from baseio import jdir
def custom_create(path, name):
    file_name = f"log.{name}.txt"
    jdir(path)
    log_file = os.path.join(path, file_name)
    formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%m/%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    screen_handler = logging.StreamHandler()
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)
    logger.setLevel(logging.INFO)
    info(f"LOGGING >>> {log_file}")

    # info("CUDA_VISIBLE_DEVICES:", os.environ["CUDA_VISIBLE_DEVICES"])
    # command("nvidia-smi")
def create(path, train):
    file_name = 'log.train.txt' if train else 'log.test.txt'
    if not os.path.exists(path):
        if train:
            os.makedirs(path)
        else:
            raise FileNotFoundError(path)
    log_file = os.path.join(path, file_name)
    formatter = logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%m/%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    screen_handler = logging.StreamHandler()
    screen_handler.setFormatter(formatter)
    logger.addHandler(screen_handler)
    logger.setLevel(logging.INFO)
    info(f"LOGGING >>> {log_file}")

    # info("CUDA_VISIBLE_DEVICES:", os.environ["CUDA_VISIBLE_DEVICES"])
    # command("nvidia-smi")

def command(cmd):
    lines = os.popen(cmd).readlines()
    lines = ''.join(lines)
    info(cmd + '\n' + lines)

def info(*msg):
    msg = ' '.join([str(_) for _ in msg])
    logging.getLogger(__name__).log(logging.INFO, msg)

def warn(*msg):
    msg = ' '.join([str(_) for _ in msg])
    logging.getLogger(__name__).log(logging.WARN, msg)

def table(rows):
    rows = [list(row) for row in rows]
    num_col = len(rows[0])
    col_lengths = [0 for _ in range(num_col)]
    for row in rows:
        for j, item in enumerate(row):
            item = to_string(item)
            row[j] = item
            if len(item) > col_lengths[j]:
                col_lengths[j] = len(item)
    outputs = []
    for i, row in enumerate(rows):
        output = ["|"]
        for j, item in enumerate(row):
            item = to_string(item)
            padding = ' ' * (col_lengths[j] - len(item))
            output.append(item + padding)
        info('\t'.join(output))
        outputs.append(output)
    return outputs

def to_string(x):
    import numpy as np
    if type(x) in [float, np.float32, np.float64]:
        return f"{x:.3f}"
    else:
        return str(x)
