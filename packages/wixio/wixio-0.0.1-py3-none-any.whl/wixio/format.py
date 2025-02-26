# -*- encoding: utf-8 -*-
"""
@File    :   format.py
@Time    :   2025/2/25 下午8:29
@Author  :   Li Jiawei
@Version :   1.0
@Contact :   Li.J.W.adrian421@hotmail.com
@License :   (C)Copyright 2023-2030
@Desc    :   None
@Brief   :
"""


class EasyDict(dict):
        """Convenience class that behaves like a dict but allows access with the attribute syntax."""

        def __getattr__(self, name: str) -> Any:
                try:
                        return self[name]
                except KeyError:
                        raise AttributeError(name)

        def __setattr__(self, name: str, value: Any) -> None:
                self[name] = value

        def __delattr__(self, name: str) -> None:
                del self[name]


def jsondump(x):
        """
        adjusted json.dumps according to
        https://blog.csdn.net/weixin_39561473/article/details/123227500
        param
        ------
        x: dict, input

        return
        ------
        res: string, json.dumps dict string
        """

        def default_dump(obj):
                """Convert numpy classes to JSON serializable objects."""
                if isinstance(obj, (np.integer, np.floating, np.bool_)):
                        return obj.item()
                elif isinstance(obj, np.ndarray):
                        return obj.tolist()
                else:
                        return obj

        res = json.dumps(x, ensure_ascii=False, default=default_dump)
        return res


def dict2class(dct, clsname='default_cls'):
        """
        Fasr converting a input dict to be a python Class

        Parameter:
        ----------
        dct: dict, any dict
        clsname: string, determine the class name for the new class

        Return:
        -------
        res: class, a new class having attributes from dict keys
        attrs: list, a list containing all attribute names
        """
        res = type(f"{clsname}", (), dct)
        attrs = list(res.__dict__.keys())
        return res, attrs


def topct(x, total):
        return round(x / total, ndigits=4) * 100


def limnum(x, out_float=1):
        """
        limit number
        """
        if out_float:
                return float(f"{x:.4f}")
        else:
                return f"{x:.4f}"



