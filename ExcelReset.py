# User: Sam
# Date: 2017/4/29
# Time: 下午9:15

import xlrd
from xlutils.copy import copy


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
                eachlist = line.split('\t')
                if len(eachlist) == 2:
                    mapdict[int(eachlist[kindex])] = int(eachlist[vindex])
            return mapdict
    except IOError as e:
        print(e)


def changetable(fT, rt, wt, pkindex, begr, begc, mapdict):
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
            ftvals = fT[rowvals[pkindex]]
            if ftvals:
                for col in range(begc, ncols):
                    try:
                        fcol = mapdict[col]
                        if fcol:
                            wt.write(row, col, ftvals[fcol])
                    except KeyError:
                        pass
        except KeyError:
            pass


def getTableDict(table, pkindex, begrow):
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
        tablerows[rowvalues[pkindex]] = rowvalues
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
    ft = getTableByIndex("fromone.xlsx", 0)
    ft = getTableDict(ft, 1, 2)
    rb = xlrd.open_workbook("lastone.xls", formatting_info=True)
    rs = rb.sheet_by_index(0)
    wb = copy(rb)
    ws = wb.get_sheet(0)
    changetable(ft, rs, ws, 1, 1, 3, fillmap)
    wb.save("./res/out2.xls")


def main():
    test()

if __name__ == '__main__':
    main()
