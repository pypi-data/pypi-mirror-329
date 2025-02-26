# -*- encoding: utf-8 -*-
"""
@File    :   metrics.py
@Time    :   2025/2/25 下午8:47
@Author  :   Li Jiawei
@Version :   1.0
@Contact :   Li.J.W.adrian421@hotmail.com
@License :   (C)Copyright 2023-2030
@Desc    :   None
@Brief   :
"""
import os, sys, argparse, numpy as np, itertools
from sklearn.metrics import precision_recall_fscore_support
from logger import write_log as logging


def f_value(y_pred, y_true, ignore=0, vocab=None, name="", is2d=False, verbose=True, very_verbose=False, \
            verbose_return=True):
        """
        Easy method to compute F1 score given results and label lists

        Parameter:
        ----------
        y_pred: list of predictions
        y_true: list of labels
        ignore: ignore some unwanted label, for example, -1
        vocab:  sometimes the labels are digits but meaning some texts,
                vocab replace digits with texts for better presentation
        name:
        is2d:
        verbose: bool, print out a table
        very_verbose: bool, print out a table
        verbose_return: bool, return p,r,f1; otherwise only return f1

        Return:
        -------
        macro and micro f1 or macro and micro p,r,f1
        """
        if is2d:
                y_pred = list(itertools.chain(*y_pred))
                y_true = list(itertools.chain(*y_true))
        labels = [_ for _ in set(y_pred + y_true) if _ != ignore]
        labels.sort()
        ps, rs, fs, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels, average=None)
        micro_p, micro_r, micro_f, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels, average="micro", warn_for=())
        macro_p, macro_r, macro_f, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels, average="macro", warn_for=())
        rows = [["Class", "N", "P", "R", "F", ""]]
        if very_verbose:
                for lab, p, r, f in zip(labels, ps, rs, fs):
                        desc = vocab.get(lab, '') if vocab is not None else ''
                        n = len([_ for _ in y_true if _ == lab])
                        rows.append([lab, n, p, r, f, desc])
        if verbose or very_verbose:
                n = len([_ for _ in y_true if _ != ignore])
                rows.append(["Macro", n, macro_p, macro_r, macro_f, ''])
                rows.append(["Micro", n, micro_p, micro_r, micro_f, ''])
                logging.info(name)
                logging.table(rows)
        if not verbose_return:
                return macro_f, micro_f
        return macro_p, macro_r, macro_f, micro_p, micro_r, micro_f


def dcg_at_k(r, k, method=0):
        """Score is discounted cumulative gain (dcg)
        Relevance is positive real values.  Can use binary
        as the previous methods.
        Example from
        http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
        >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
        >>> dcg_at_k(r, 1)
        3.0
        >>> dcg_at_k(r, 1, method=1)
        3.0
        >>> dcg_at_k(r, 2)
        5.0
        >>> dcg_at_k(r, 2, method=1)
        4.2618595071429155
        >>> dcg_at_k(r, 10)
        9.6051177391888114
        >>> dcg_at_k(r, 11)
        9.6051177391888114
        Args:
            r: Relevance scores (list or numpy) in rank order
                (first element is the first item)
            k: Number of results to consider
            method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                    If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
        Returns:
            Discounted cumulative gain
        """
        r = np.asfarray(r)[:k]
        if r.size:
                if method == 0:
                        return r[0] + np.sum(r[1:] / np.log2(np.arange(3, r.size + 2)))  # fix here
                elif method == 1:
                        return np.sum(r / np.log2(np.arange(2, r.size + 2)))
                else:
                        raise ValueError('method must be 0 or 1.')
        return 0.


def ndcg_at_k(r, k, method=0):
        """Score is normalized discounted cumulative gain (ndcg)
        Relevance is positive real values.  Can use binary
        as the previous methods.
        Example from
        http://www.stanford.edu/class/cs276/handouts/EvaluationNew-handout-6-per.pdf
        >>> r = [3, 2, 3, 0, 0, 1, 2, 2, 3, 0]
        >>> ndcg_at_k(r, 1)
        1.0
        >>> r = [2, 1, 2, 0]
        >>> ndcg_at_k(r, 4)
        0.9203032077642922
        >>> ndcg_at_k(r, 4, method=1)
        0.96519546960144276
        >>> ndcg_at_k([0], 1)
        0.0
        >>> ndcg_at_k([1], 2)
        1.0
        Args:
            r: Relevance scores (list or numpy) in rank order
                (first element is the first item)
            k: Number of results to consider
            method: If 0 then weights are [1.0, 1.0, 0.6309, 0.5, 0.4307, ...]
                    If 1 then weights are [1.0, 0.6309, 0.5, 0.4307, ...]
        Returns:
            Normalized discounted cumulative gain
        """
        dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
        if not dcg_max:
                return 0.
        return dcg_at_k(r, k, method) / dcg_max
