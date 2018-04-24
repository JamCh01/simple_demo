import csv
import sys
import codecs
import tempfile
import requests
from bs4 import BeautifulSoup


def url_generator(keyword):
    return 'https://search.jd.com/Search?keyword={keyword}&enc=utf-8'.format(
        keyword=keyword)


def spider(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:58.0) Gecko/20100101 Firefox/58.0',
        'Referer':
        'https://www.jd.com/',
        'Host':
        'search.jd.com',
    }
    r = requests.get(url=url, headers=headers)
    r.encoding = 'utf8'
    return r.text


def html_parse(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.find_all('li', {'class': 'gl-item'})


def data_parse(targets):
    result = list()
    result.append(['商品名称', '价格', '商店名称', '是否自营', '累计评价数', '商品地址', '商品图片地址'])
    for target in targets:
        try:
            title = target.find('div', {
                'class': 'p-name p-name-type-2'
            }).find('em').text
        except AttributeError as e:
            title = ''

        try:
            price = target.find('div', {'class': 'p-price'}).find('i').text
        except AttributeError as e:
            price = ''

        try:
            commits = target.find('div', {'class': 'p-commit'}).find('a').text
        except AttributeError as e:
            commits = ''

        try:
            shop = target.find('div', {'class': 'p-shop'}).find('a').text
        except AttributeError as e:
            shop = ''
        try:
            if '自营' in target.find('div', {'class': 'p-icons'}).text:
                self_employed = True
            else:
                self_employed = False
        except AttributeError as e:
            self_employed = False

        try:
            img = target.find('div', {'class': 'p-img'}).find('img')['src']
        except KeyError:
            img = target.find('div', {
                'class': 'p-img'
            }).find('img')['data-lazy-img']
        except AttributeError:
            img = ''
        try:
            goods_url = target.find('div', {
                'class': 'p-name p-name-type-2'
            }).find('a')['href']
        except AttributeError:
            goods_url = ''
        result.append([
            title,
            price,
            shop,
            self_employed,
            commits,
            'https:{goods_url}'.format(goods_url=goods_url),
            'https:{img}'.format(img=img),
        ])
    return result


def out_path():
    return tempfile.mktemp(".csv", prefix="jd_")


def write_csv(data):
    out = out_path()
    if sys.platform == 'win32':
        with open(out, 'wb') as f:
            f.write(codecs.BOM_UTF8)
        csv_mode = 'a'
    else:
        csv_mode = 'w'
    with open(out, csv_mode, encoding='utf8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    return out


def main():
    url = url_generator(keyword='进口牛奶')
    html = spider(url=url)
    target = html_parse(html)
    data = data_parse(targets=target)
    print(write_csv(data=data))


if __name__ == '__main__':
    main()