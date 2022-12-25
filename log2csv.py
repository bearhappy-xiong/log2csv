import csv
import os
import re
import sys
from collections.abc import Iterable
from io import StringIO

from pandas import DataFrame

FIELD_NAMES = [
    "episode",
    "episode_reward",
    "step",
]

def log2csv(inputfilepath, outputfilepath=None):
    if outputfilepath is None:
        outputfilepath = os.path.join(os.path.dirname(inputfilepath), "eval.csv")
    else:
        outputfilepath = outputfilepath
    """
    也可以使用replace来替换文件扩展名.
    使用replace方法的一个优点是，如果你的文件扩展名不是".log"，它仍然可以正常工作。
    例如，如果你的文件扩展名是".txt"，那么代码仍然会将其替换为".csv"。

    但是，使用os.path.join和os.path.dirname的优点是，它们更通用，
    可以用于任何操作系统，而不仅仅是Windows。
    """
    # TODO - 添加对子文件夹的支持

    if not os.path.isfile(inputfilepath):
        print("error message :", f"'{inputfilepath}' file does not exist")
        sys.exit(2)

    rows = []
    with open(inputfilepath) as f:
        for row in csv.reader(f, delimiter=' '):
            rows.append(Log2Csv(row).to_dict(field_names=FIELD_NAMES))

    df = DataFrame(rows)
    df.to_csv(outputfilepath, index=False, columns=FIELD_NAMES, header=FIELD_NAMES,
              encoding='utf-8')

    print("COMPLETE CONVERTING LOG TO CSV")


class Log2Csv(object):
    def __init__(self, single_line):
        self.field_names = FIELD_NAMES
        self.data = {}
        if type(single_line) is str:
            buff = StringIO(single_line)  # 将字符串转换为文件对象
            single_line = next(csv.reader(buff, delimiter=' '))  # 将文件对象转换为列表
        if isinstance(single_line, Iterable):  # 如果每行数据是列表
            # 提取出列表中的字符串形式的数字
            i = -1
            for field_name in self.field_names:
                # 下面的写法对应于这样的single_line: 
                # ['episode', '0', 'episodeReward', '0.0', 'step', '0']
                i = i+2  # i会取值1, 3, 5
                self.data.update({field_name: single_line[i]})

    def __getitem__(self, item):
        if item in self.data:
            return self.data[item]
        else:  # access to custom fields by property
            r = getattr(self, item, None)
            if type(r) is callable:
                return None
            return r

    def to_dict(self, field_names):
        ret = {}
        for field_name in field_names:
            # self[field_name]这个写法其实是调用了__getitem__方法
            if self[field_name]:
                # 使用re库中的正则表达式提取出字符串中的数字(Re库是Python的标准库，主要用于字符串匹配)
                # 这个正值表达式的意思是匹配出字符串中的数字，包括小数
                temp = re.findall(r"\d+\.?\d*",self[field_name])
                t = temp[0]  # 提取出的是一个列表，但是实质上只有一个元素, 取出来.
                if field_name == 'episode':
                    ret.update({str(field_name): int(float(t))})
                if field_name == 'episode_reward':
                    ret.update({str(field_name): float(t)})
                if field_name == 'step':
                    ret.update({str(field_name): int(t)})
        return ret


if __name__ == "__main__":
    inputfilepath = os.getcwd()
    outputfilepath = None
    log2csv(inputfilepath, outputfilepath)