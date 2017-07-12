# User: ddsss
# Date: 2017/7/9
# Time: 下午1:45
import xlrd
from xlutils.copy import copy
import re
import ExcelReset
import os


def getValFromExcel(rt, appendx, vallist, regx, keyrow, begcol, resmap=None):
    """
    :type rt xlrd.Sheet 
    :param valmap dict
    :return: 
    """
    if resmap is None:
        resmap = {}
    keys1 = rt.row_values(keyrow)[begcol:]
    keys = []
    for x in keys1:
        x = x.replace(" ", "")
        keys.append(x)
    vals = {}
    tempvals = rt.col_values(0)
    for i in range(len(tempvals)):
        temp = tempvals[i]
        if regx.match(str(tempvals[i])):
            if tempvals[i] in vallist:
                rowvals = rt.row_values(i)[begcol:]
                for j in range(len(keys)):
                    try:
                        vildict = resmap[appendx + keys[j]]
                    except KeyError:
                        vildict = {}
                        resmap[appendx + keys[j]] = vildict
                    vildict[tempvals[i]] = rowvals[j]
    return resmap


def demo():
    ft = ExcelReset.getTableByIndex("data/clearData/上营乡/基5.xls", 0)
    whitelist = ["025800", "026200", "027700", "099800", "160010", "160330", "013300"]
    regx = re.compile("^\d+$")
    res = getValFromExcel(ft, "a", whitelist, regx, 8, 4)
    ft2 = ExcelReset.getTableByIndex("data/clearData/a/a.xls", 0)
    res = getValFromExcel(ft2, "a", whitelist, regx, 8, 4, res)
    print(res)


def demo2(path):
    res = {}
    whitelist = ["025800", "026200", "027700", "099800", "160010", "160330", "013300"]
    regx = re.compile("^\d+$")
    for each in os.listdir(path):
        dirpath = os.path.join(path, each)
        if os.path.isdir(dirpath):
            for root, dirs, files in os.walk(dirpath):
                for eachxls in files:
                    if eachxls.endswith(".xls"):
                        ft = ExcelReset.getTableByIndex(os.path.join(root, eachxls), 0)
                        res = getValFromExcel(ft,each, whitelist, regx, 8, 4, res)
    return res


if __name__ == '__main__':
    res = demo2("data/clearData")
    print(res)
    print(len(res))
