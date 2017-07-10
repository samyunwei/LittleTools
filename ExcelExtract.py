# User: ddsss
# Date: 2017/7/9
# Time: 下午1:45
import xlrd
from xlutils.copy import copy


def getValFromExcel(rt, valmap, keyrow, begcol, resmap=None):
    """
    :type rt xlrd.Sheet 
    :param valmap dict
    :return: 
    """
    if resmap is None:
        resmap = {}
    keys = rt.row_values(keyrow)[begcol:]
    vals = {}
    for eachkey in valmap:
        vals[eachkey] = rt.row_values(eachkey)[begcol:]
    for i in range(keys):
        attrs = {}
        for eachvalkey in vals:
            attrs[eachvalkey] = vals[eachvalkey][i]
        resmap[keys[i]].update(attrs)
    return resmap
