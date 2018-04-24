import csv
import sys
import queue
import codecs
import tempfile
import requests
from functools import partial
from multiprocessing.dummy import Pool

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
COUNT_PAGE = 114

TMP = list()
TMP.append(['股票代码', '股票名称', '当前价', '涨跌幅', '市值', '市盈率'])


def cookie_generator():
    url = 'https://xueqiu.com/'
    s = requests.session()
    r = s.get(url=url, headers=HEADERS)
    return s


def api_url_generator():
    base_url = 'https://xueqiu.com/stock/cata/stocklist.json?page={page_num}&size=100&order=desc&orderby=percent&type=0,1,2,3&isdelay=1&_=1524557742742'
    return [base_url.format(page_num=i) for i in range(1, COUNT_PAGE + 1)]


def api_crawler(s, url):
    #股票代码，股票名称，当前价，涨跌幅，市值，市盈率
    r = s.get(url=url, headers=HEADERS)
    result = r.json().get('stocks')
    for i in result:
        ret = [
            i.get('code'),
            i.get('name'),
            i.get('current'),
            i.get('percent'),
            i.get('marketcapital'),
            i.get('pettm')
        ]
        TMP.append(ret)


def out_path():
    return tempfile.mktemp(".csv", prefix="xueqiu_")


def init_csv(out):
    with open(out, 'wb') as f:
        f.write(codecs.BOM_UTF8)


def write_csv(out, data):
    with open(out, 'a', encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def main():
    p = Pool(20)
    s = cookie_generator()
    urls = api_url_generator()
    crawler = partial(api_crawler, s)
    ret = p.map_async(crawler, urls)
    ret.wait()
    out = out_path()
    init_csv(out=out)
    write_csv(out=out, data=TMP)
    return out


if __name__ == '__main__':
    main()
