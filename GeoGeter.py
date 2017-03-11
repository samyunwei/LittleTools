import xlrd
from villiage import villiage
from urllib import request, parse
from os import path
from myconfig import my_token
from myconfig import APIURL


def getvilliageFromSheets(sheetname, index_sheet, index_town, index_villiage, br=0, er=None):
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
    for eachvil in vils:
        handle = request.urlopen(getSearchStrByTarget(eachvil))
        res = handle.read()
        eachvil.geojson = res.decode("utf8")
        print(str(eachvil) + "GetOne")
    return vils


def saveVilInfoInFile(filename, vils):
    print(len(vils))
    if path.exists(filename):
        raise ValueError
    else:
        with open(filename, 'w+') as f:
            for each in vils:
                f.write(each.getSaveStr())


def setvil(vils, city, county):
    """
    :type vil:villiage
    :param city:
    :param county:
    :return:
    """
    for vil in vils:
        vil.city = city
        vil.county = county
    return vils


def getvilliageInfotofile():
    vils = getvilliageFromSheets("data.xlsx", 4, 0, 1, 1)
    setvil(vils, "定西市", "临洮县")
    getVilliageInfoFromWeb(vils)
    saveVilInfoInFile("data2.txt", vils)


def getVilFromDataFile(filename):
    vils = []
    with open(filename, 'r') as f:
        for eachline in f:
            vils.append(villiage.getVilFromString(eachline.strip()))
    for eachvil in vils:
        eachvil.setDict()
        print(eachvil.name, eachvil.longitude)


"""
    Some Test for function
"""


def test():
    #getvilliageInfotofile()
    getVilFromDataFile("test.txt")


"""
    Main
"""


def main():
    test()


if __name__ == '__main__':
    main()
