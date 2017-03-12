import xlrd
from villiage import villiage
from urllib import request, parse
from os import path
import xlwt
from myconfig import my_token
from myconfig import APIURL
from myconfig import Searcg_County, Search_City


def getvilliageFromSheets(sheetname, index_sheet, index_town, index_villiage, br=0, er=None):
    """
    get vils from execl.
    :param sheetname:vils sheet name
    :param index_sheet: vil's sheet index
    :param index_town: vil' town name
    :param index_villiage: vil's index
    :param br: the index for begin row
    :param er: the index for end row
    :return: vils
    """
    data = xlrd.open_workbook(sheetname)
    table = data.sheet_by_index(index_sheet)
    res = []
    if er is None:
        er = table.nrows
    for i in range(br, er):
        row = table.row(i)
        vilname = row[index_villiage].value.strip().replace(" ", "")
        if "村" not in vilname:
            vilname += "村"
        newvi = villiage(vilname, row[index_town].value.strip())
        res.append(newvi)
    return res


def getSearchStrByTarget(target, token=my_token):
    """

    :param target:
    :type target:villiage
    :return:
    """
    tardict = target.getSerachDict()
    tardict["key"] = my_token
    return APIURL % parse.urlencode(tardict)


def getVilliageInfoFromWeb(vils):
    """
    Use GAODE API to get JSON info.
    :param vils:the vils to be search
    :return: the vils.
    """
    for eachvil in vils:
        handle = request.urlopen(getSearchStrByTarget(eachvil))
        res = handle.read()
        eachvil.geojson = res.decode("utf8")
        print(str(eachvil) + "GetOne")
    return vils


def saveVilInfoInFile(filename, vils, overwrite=False):
    """
    Save Vils Info Into files.If the file has existed it will raise value Error.
    :param filename: thefilename was  saved.
    :param vils:
    :param overwrite: if has the same name file,overwritten it
    :return: void
    """
    if path.exists(filename) and not overwrite:
        raise ValueError
    else:
        with open(filename, 'w+') as f:
            for each in vils:
                f.write(each.getSaveStr())


def setvil(vils, city, county):
    """
    set vils city and county value.
    :type vil:villiage
    :param city:
    :param county:
    :return:
    """
    for vil in vils:
        vil.city = city
        vil.county = county
    return vils


def getVilFromDataFile(filename):
    """
    Get vils info from file
    :param filename:
    :return:
    """
    vils = []
    with open(filename, 'r') as f:
        for eachline in f:
            vils.append(villiage.getVilFromString(eachline.strip()))
    for eachvil in vils:
        eachvil.setDict()
    return vils


def SaveVilsTotxtByAttr(vals, filename, overwriteflag, *attr):
    """
    save vils info into txt.
    :param vals:
    :param filename:
    :param overwriteflag:
    :param attr:
    :return:
    """
    if path.exists(filename) and not overwriteflag:
        raise ValueError("File have already exist")
    else:
        saverstr = "%-15s" * len(attr) + "\n"
        with open(filename, 'w+') as f:
            f.write(saverstr % tuple(attr))
            for each in vals:
                attrstr = list(map(lambda x: getattr(each, x), attr))
                f.write(saverstr % tuple(attrstr))


def saveVilsToExcelByAttr(vals, filename, overwriteflag, *attr):
    """
    save vils info into excel
    :param vals:
    :param filename:
    :param overwriteflag:
    :param attr:
    :return:
    """
    if path.exists(filename) and not overwriteflag:
        raise ValueError("File have already exist")
    f = xlwt.Workbook()
    sheet = f.add_sheet("sheet1", cell_overwrite_ok=True)
    for col in range(len(attr)):
        sheet.write(0, col, attr[col])
    for row in range(len(vals)):
        attrstr = list(map(lambda x: getattr(vals[row], x), attr))
        for eachc in range(len(attrstr)):
            sheet.write(1 + row, eachc, attrstr[eachc])
    f.save(filename)


"""
    Some Test for function
"""


def testvilliageInfotofile():
    vils = getvilliageFromSheets("data.xlsx", 4, 0, 1, 1)
    setvil(vils, Search_City, Searcg_County)
    getVilliageInfoFromWeb(vils)
    saveVilInfoInFile("data2.txt", vils)


def test():
    # tetstvilliageInfotofile()
    # vals = getVilFromDataFile("data2.txt")
    # SaveVilsTotxtByAttr(vals, "res.txt", True, "town", "name", "longitude", "latitude", "isConfirm")
    # saveVilsToExcelByAttr(vals, "res2.xls", True, "town", "name", "longitude", "latitude", "isConfirm")
    pass


"""
    Main
"""


def main():
    test()


if __name__ == '__main__':
    main()
