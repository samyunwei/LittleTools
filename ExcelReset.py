# User: Sam
# Date: 2017/4/29
# Time: 下午9:15

import xlrd
from xlutils.copy import copy
import os
import ExcelExtract
def getMaps(file, kindex, vindex):
    """
    This func use for reading map from *.csv
    :param file: csv file
    :return:map
    @type file:string
    """
    if not file.endswith(".csv"):
        raise IOError("must csv file")
    mapdict = {}
    try:
        with open(file) as f:
            for eachline in f:
                line = eachline.strip()
                eachlist = line.split("\t")
                if len(eachlist) == 2:
                    mapdict[int(eachlist[kindex])] = int(eachlist[vindex])
            return mapdict
    except IOError as e:
        print(e)


def changetable(fT, rt, wt, pkindexes, begr, begc, mapdict):
    """
    According to ft map change rt
    :param ft map
    :param rt the table was filled
    :param pkindex pk
    :param mapdict the *.csv map
    :type mapdict dict
    :type rt xlrd.Sheet
    """
    nrows = rt.nrows
    ncols = rt.ncols
    for row in range(begr, nrows):
        rowvals = rt.row_values(row)
        try:
            key = ""
            for eachindex in pkindexes:
                key += rowvals[eachindex]
            ftvals = fT[key]
            if ftvals:
                for col in range(begc, ncols):
                    try:
                        fcol = mapdict[col]
                        if fcol:
                            wt.write(row, col, ftvals[fcol])
                    except KeyError:
                        pass
        except KeyError:
            print("No found Key:" + key)
            pass


def getTableDict(table, pkindexes, begrow):
    """
    
    :param table: excel sheet
    :param pkindex:
    :param begrow: 
    :return:
    :type table xlrd.Sheet
    """
    tablerows = {}
    nrows = table.nrows
    for row in range(begrow, nrows):
        rowvalues = table.row_values(row)
        key = ""
        for eachindex in pkindexes:
            key += rowvalues[eachindex]
        if tablerows.__contains__(key):
            print(key, row)
        tablerows[key] = rowvalues
    return tablerows


def getTableByIndex(file, index, formatinfo=False):
    """
    :param file: xls or xlsx file 
    :param index:sheet index
    :param formatinfo: 
    :return: 
    """
    data = xlrd.open_workbook(file, formatting_info=formatinfo)
    return data.sheet_by_index(index)


def test():
    """
    test func
    :return: 
    """
    fillmap = getMaps("data/map.csv", 1, 0)
    ft = getTableByIndex("data/土壤对应表.xlsx", 0)
    ft = getTableDict(ft, [0, 1], 2)
    ft2 = {}
    for eachkey in ft:
        ft2[eachkey.replace("村", "")] = ft[eachkey]
    rb = xlrd.open_workbook("data/lastone.xls", formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    changetable(ft, rs, ws, [0, 1], 1, 3, fillmap)
    changetable(ft2, rs, ws, [0, 1], 1, 3, fillmap)
    wb.save("./res/out3.xls")
    print(len(ft.keys()))


def demo2():
    fillmap = getMaps("data/map2.csv", 1, 0)
    ft = getTableByIndex("data/data2.xls", 0)
    print(fillmap)
    ft = getTableDict(ft, [1, 2], 3)
    ft2 = {}
    for eachkey in ft:
        ft2[eachkey.replace("村民委员会", "")] = ft[eachkey]
    ft3 = {}
    for eachkey in ft:
        ft3[eachkey.replace("民委员会", "")] = ft[eachkey]

    print(ft2.keys())
    rb = xlrd.open_workbook("data/终极表2.xls", formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    changetable(ft2, rs, ws, [0, 1], 2, 3, fillmap)
    changetable(ft3, rs, ws, [0, 1], 2, 3, fillmap)
    wb.save("./res/out3.xls")
    print(len(ft.keys()))


def demo3():
    ft = ExcelExtract.demo2("data/clearData")
    mapdict = {}
    ft2 = {}
    for eachkey in ft:
        ft2[eachkey + "村"] = ft[eachkey]
    ft3 = {}
    for eachkey in ft:
        ft3[eachkey.replace("村", "")] = ft[eachkey]
    rb = xlrd.open_workbook("data/data3.xls", formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    changetable(ft, rs, ws, [0, 1], 1, 3,mapdict)
    changetable(ft2, rs, ws, [0, 1], 1, 3, mapdict)
    changetable(ft3, rs, ws, [0, 1], 1, 3, mapdict)
    wb.save("./res/roughres.xls")
    print(len(ft.keys()))


def main():
    # test()
    #demo2()
    demo3()


if __name__ == '__main__':
    main()
