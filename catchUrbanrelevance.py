# -*- coding: utf-8 -*-
# 采集SERP搜索结果标题
from urllib import request, parse
from bs4 import BeautifulSoup
import string
import time
import re
import codecs

__doc__ = """
    获得城市间大地重力系数。好早之前，用2.7写的 改了一下用3.X，目前没有测试，只是备份。
"""


# 写文件
def WriteFile(fileName, content):
    try:
        fp = open(fileName, "a+")
        fp.write(content + "\r")
        fp.close()
    except:
        pass


# 获取Html源码
def GetHtml(url):
    data = None
    try:
        req = parse.quote(url)
        response = request.urlopen(req, None, 10)  # 设置超时时间
        data = response.read().decode('utf-8', 'ignore')
    except Exception as e:
        print(e)
        pass
    return data


# 提取搜索结果SERP的标题
def FetchTitle(html):
    try:
        soup = BeautifulSoup(''.join(html))
        '''count = 0
        for i in soup.findAll("h3"):
            title = i.text.encode("utf-8")
            if any(str_ in title for str_ in ("2015","2016")):
                continue
            else:
                count+= 1
                print count
            WriteFile("Result.txt",title)
        '''

        for i in soup.findAll("span"):
            countstr = i.text.encode("utf-8")
            if "相关新闻" in countstr:
                catchcount = re.compile(r'\d+')
                count = catchcount.search(countstr)
                print(countstr)
                return count.group()

    except:
        pass


def Geturl(theCity1, theCity2, theBegin_Time, theEndTime, theall=True):
    if theall:
        theCity1 = theCity1.decode('utf8', 'replace')
        theCity2 = theCity2.decode('utf8', 'replace')
        theCity1 = theCity1.encode('gbk', 'replace')
        theCity2 = theCity2.encode('gbk', 'replace')

        code_city1 = "%22" + parse.quote(theCity1, safe=string.printable)
        code_city2 = parse.quote(theCity2, safe=string.printable) + "%22"
    else:
        theCity1 = theCity1.decode('utf8', 'replace')
        theCity2 = theCity2.decode('utf8', 'replace')
        theCity1 = theCity1.encode('gbk', 'replace')
        theCity2 = theCity2.encode('gbk', 'replace')

        code_city1 = parse.quote(theCity1, safe=string.printable)
        code_city2 = parse.quote(theCity2, safe=string.printable)

    tl1 = theBegin_Time.split('-')
    tl2 = theEndTime.split('-')

    # ts1 = str(time.mktime((int(tl1[0])-1,12,31,23,59,59,0,0,0)))
    ts1 = str(time.mktime((int(tl1[0]), 1, 1, 0, 0, 0, 0, 0, 0)))
    ts2 = str(time.mktime((int(tl2[0]), 12, 31, 23, 59, 59, 0, 0, 0)))

    url = 'http://news.baidu.com/ns?from=news&cl=2&bt=' + ts1 + '&y0=' + tl1[0] + '&m0=1&d0=1&y1=' + tl2[
        0] + '&m1=12&d1=31&et=' + ts2 + '&q1=' + code_city1 + "+" + code_city2 + '&submit=%B0%D9%B6%C8%D2%BB%CF%C2&q3=&q4=&mt=0&lm=&s=2&begin_date=' + theBegin_Time + '&end_date=' + theEndTime + '&tn=newsdy&ct1=1&ct=1&rn=20&q6='

    return url


def GetConnect(theCity1, theCity2, theby, theey):
    result = []
    result.append(theCity1)
    result.append(theCity2)
    for i in range(theby, theey):
        url = Geturl(theCity1, theCity2, str(i) + '-1-1', str(i) + '-12-31')
        html = GetHtml(url)
        while html == None:
            html = GetHtml(url)
        print(url)
        print(i, sep="")
        theconnect = str(FetchTitle(html))
        print(theconnect)
        result.append(theconnect)
        # time.sleep(1)
    return result


def WriteResult(theResult):
    with open('myresultzhaoqing.txt', 'a') as myresult:
        for eachitem in theResult:
            myresult.write(eachitem + '\t')
        myresult.write('\n')


if __name__ == "__main__":
    start = time.time()
    citys = []
    with codecs.open('mycity3.txt', 'r', encoding='utf-8') as fcitys:
        item = fcitys.readline().strip()
        while item:
            citys.append(item)
            item = fcitys.readline().strip()
            print(item)

    for eachcity in citys:
        WriteResult(GetConnect('xx市', eachcity.encode('utf-8'), 2000, 2016))
        print(eachcity)
    c = time.time() - start
    print('程序运行耗时:%0.2f 秒' % (c))
