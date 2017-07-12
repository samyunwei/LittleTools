import pandas as pd
import os
import shutil
import re
from functools import partial


def TransFormExcel(file, outfile):
    df = pd.read_excel(file)
    df_T = df.T
    df_T.to_excel(outfile, sheet_name="sheet_1")


def MoveFile(rootpath, changeFunc, suffix):
    for eachfile in os.listdir(rootpath):
        eachdirpath = os.path.join(rootpath, eachfile)
        if os.path.isdir(eachdirpath):
            outdir = changeFunc(eachfile)
            os.makedirs(outdir)
            for root, dirs, files in os.walk(eachdirpath):
                for name in files:
                    if name.endswith(suffix):
                        shutil.copy(os.path.join(root, name), outdir + os.sep)
        else:
            print(eachfile)
            print(os.path.isdir(eachfile))


def FiliterFile(rootpath, whitelist, suffix):
    for root, dirs, files in os.walk(rootpath):
        for name in files:
            name = name.replace(suffix, "")
            if name not in whitelist:
                filepath = os.path.join(root, name)+ suffix
                os.remove(filepath)
                print("remove:" + filepath)
            else:
                print("save"+name)


def extractName(dirname, outdir, regx, tag):
    """
    :param dirname:
    :param outdir:
    :param regx:
    :return:
    """
    pattern = regx.match(dirname)
    if pattern:
        tagname = pattern.groupdict()[tag]
    else:
        print(dirname)
        raise ValueError
    res = ""
    if outdir:
        res = outdir + os.sep + tagname
    else:
        res = tagname
    return res


def testRegx():
    vilregx = re.compile("(\d*)(?P<vilname>[\u4e00-\u9fa5]+[镇乡])(\d?[\u4e00-\u9fa5]?)")
    for eachfile in os.listdir("test"):
        vilname = vilregx.match(eachfile)
        if vilname:
            print(vilname.groupdict()["vilname"])
        else:
            print("Not found" + eachfile)


def demo():
    vilregx = re.compile("(\d*)(?P<vilname>[\u4e00-\u9fa5]+[镇乡])(\d?[\u4e00-\u9fa5]?)")
    Myextractfunc = partial(extractName, outdir="data" + os.sep + "clearData", regx=vilregx, tag="vilname")
    for eachfile in os.listdir("data" + os.sep + "test"):
        res = Myextractfunc(eachfile)
        print(res)
    MoveFile(("data" + os.sep + "test"), Myextractfunc, ".xls")


def demo2():
    whitelist = ["a","b"]
    FiliterFile("data" + os.sep + "clearData",whitelist,".xls")

if __name__ == '__main__':
    demo2()
