# -*- coding: utf-8 -*-
_author__ = 'Administrator'

import requests
from requests.exceptions import RequestException
import re
import json


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile('class="site-piclist_info_title ".*?title="(.*?)".*?href="(.*?)"', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '电视剧名称': item[0],
            'URL': item[1],
        }


def parse_detail_page(html):
    pattern = re.compile('class="site-piclist_info_title".*?href="(.*?)".*?target="_blank">.*?(\d+).*?</a>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'url': item[0],
            '集数': item[1],
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(page_num):
    url = 'http://list.iqiyi.com/www/2/-------------11-{0}-1-iqiyi--.html'.format(page_num)
    print('url',url)
    html = get_one_page(url)
    rets = parse_one_page(html)
    # print('html', html)
    for ret in rets:
        html = get_one_page(ret['URL'])
        r = ret['电视剧名称']
        write_to_file(r)
        rets2 = parse_detail_page(html)
        for ret2 in rets2:
            r = '第{0}集${1}$qiyi'.format(ret2['集数'], ret2['url'])
            write_to_file(r)


if __name__ == '__main__':
    for i in range(1, 31):
        main(i)


