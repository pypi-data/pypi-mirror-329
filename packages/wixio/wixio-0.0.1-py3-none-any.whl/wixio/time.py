# -*- encoding: utf-8 -*-
"""
@File    :   time.py
@Time    :   2025/2/25 下午8:36
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


def get_time_dif(start_time):
        """获取已使用时间"""
        end_time = time.time()
        time_dif = end_time - start_time
        return timedelta(seconds=int(round(time_dif)))


class msTimer(object):
        @staticmethod
        def set():
                t1 = datetime.datetime.now().microsecond
                t3 = time.mktime(datetime.datetime.now().timetuple())
                return t1, t3

        @staticmethod
        def get(t1, t3, out=False):
                t2 = datetime.datetime.now().microsecond
                t4 = time.mktime(datetime.datetime.now().timetuple())
                strTime = ((t4 - t3) * 1000 + (t2 - t1) / 1000)
                print(f"\ntime passed:{strTime:.3f}ms\n")
                if out:
                        return strTime


def TimeStampToTime(timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


class GetDateStr:
        @staticmethod
        def time_now():
                return datetime.datetime.now()

        @staticmethod
        def get_x_days_ago(x):
                """
                Get the string of date of x days ago, forms like '20220101'

                Parameter:
                ----------
                x: int, determine a days number

                Return:
                -------
                string of the date of x days ago
                """
                now = datetime.datetime.now()
                return (now - datetime.timedelta(days=x)).strftime("%Y%m%d")

        @staticmethod
        def get_today():
                """
                [usage]:
                    [input]:
                        * null
                    [output]:
                        * yesterday: String, 20200801
                """
                now = datetime.datetime.now()
                return now.strftime("%Y%m%d")

        @staticmethod
        def compute_day_differs(target_date):  # target_date = "20210101"
                """
                Rodrigues' rotation formula that turns axis-angle tensor into rotation
                matrix in a batch-ed manner.

                Parameter:
                ----------
                r: Axis-angle rotation tensor of shape [batch_size, 1, 3].

                Return:
                -------
                Rotation matrix of shape [batch_size, 3, 3].
                """
                examine_days_ago = datetime.date.today().__sub__(datetime.date(int(target_date[:4]), int(target_date[4:6]), int(target_date[6:]))).days
                return examine_days_ago

        @staticmethod
        def compute_date_differs(date1, date2):  # target_date = "20210101"
                """
                Rodrigues' rotation formula that turns axis-angle tensor into rotation
                matrix in a batch-ed manner.

                Parameter:
                ----------
                r: Axis-angle rotation tensor of shape [batch_size, 1, 3].

                Return:
                -------
                Rotation matrix of shape [batch_size, 3, 3].
                """
                differ_days = datetime.date(int(date2[:4]), int(date2[4:6]), int(date2[6:])).__sub__(datetime.date(int(date1[:4]), int(date1[4:6]), int(date1[6:]))).days
                return differ_days

        @staticmethod
        def get_x_days_ago_from_target(target_dt, days):
                """
                Rodrigues' rotation formula that turns axis-angle tensor into rotation
                matrix in a batch-ed manner.

                Parameter:
                ----------
                target_dt: a target date, form like '20220103'
                days, an int, represent N days ago from target_dt, if set to 2, then the result is '20220101'

                Return:
                -------
                dt string
                """
                assert isinstance(target_dt, str), f"target_dt should be string, instead got {target_dt}"
                days = int(days) if not isinstance(days, int) else days
                return GetDateStr.get_x_days_ago(days + GetDateStr.compute_day_differs(target_dt))

        @staticmethod
        def ts_to_hours(ts):
                """
                Rodrigues' rotation formula that turns axis-angle tensor into rotation
                matrix in a batch-ed manner.

                Parameter:
                ----------
                r: Axis-angle rotation tensor of shape [batch_size, 1, 3].

                Return:
                -------
                Rotation matrix of shape [batch_size, 3, 3].
                """
                time_struct = time.localtime(ts)
                time_result = f"{time_struct.tm_year}.{time_struct.tm_mon}.{time_struct.tm_mday}-{time_struct.tm_hour}:{time_struct.tm_min}:{time_struct.tm_sec}-weekday={time_struct.tm_wday}.yearday={time_struct.tm_yday}"
                time_flag = "unknown"

                if 6 <= time_struct.tm_hour < 12:
                        time_flag = "morning"
                if 12 <= time_struct.tm_hour < 15:
                        time_flag = "noon"
                if 15 <= time_struct.tm_hour < 18:
                        time_flag = "afternoon"
                if 18 <= time_struct.tm_hour < 21:
                        time_flag = "evening"
                if 21 <= time_struct.tm_hour < 24 or 0 <= time_struct.tm_hour < 6:
                        time_flag = "night"

                return time_flag, time_result


def TimeStampToTime(timestamp):
        timeStruct = time.localtime(timestamp)
        return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def date_range(start_date, end_date):
        '''
        dates = date_range('20210701','20210705')
        for date in dates:
            print(date)
        '''
        ds = datetime.datetime.strptime(start_date, '%Y%m%d')
        de = datetime.datetime.strptime(end_date, '%Y%m%d')
        delta = (de - ds).days
        dates = [ds + datetime.timedelta(days=i) for i in range(delta)]
        dates = [date.strftime('%Y%m%d') for date in dates]
        return dates
