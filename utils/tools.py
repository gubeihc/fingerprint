import argparse
import json
import re
import ast
import operator
import csv


# 读取指纹文件
def readfilelist():
    with open("data/cms.json", 'r') as f:
        mark_list = json.load(f)
    jsonlist = sorted(mark_list, key=operator.itemgetter('flag'), reverse=True)
    return jsonlist


# 更新指纹文件
def updatefilelist(data):
    with open("data/cms.json", 'w') as f:
        json.dump(data, f, ensure_ascii=False)


# 读取批量扫描的文件
def readurlfile(filename):
    with open(filename, 'r', encoding='utf-8') as fp:
        wordlist = fp.read().splitlines()
        urls = set(
            url.strip() if url.strip().startswith(('http://', 'https://')) else ''.join(('http://', url.strip()))
            for url in wordlist if len(url) > 1)
    return urls


# 通过正则匹配 获取title
async def titles_html(html):
    titles = (
        "<titlename='school'class=\"i18n\">(.*)</title>",
        'document.title\s=\s"(.*?)"',
        'document.title="(.*?)"',
        '<title>(.*?)</title>',
        '<titlet="(.*?)"></title>',
        '<title class="next-head">(.*?)</title>',
        '<h1 class="l logo">(.*)</h1>',
    )
    html = html.replace(' ', '')
    for ti in titles:
        title = re.findall(ti, html, re.S | re.I)
        if len(title) == 0:
            pass
        elif len(title) >= 1:
            if len(title[0]) >= 1:
                titlename = str(title[0]).replace('\r', '').replace('\n', '').strip()
                return titlename
            elif len(title) >= 2:
                titlename = str(title[1]).replace('\r', '').replace('\n', '').strip()
                return titlename


class FingerPrintcms(object):
    def __init__(self):
        self.fingerprintlist = readfilelist()

    def astz(self, title, header, body):
        for index, item in enumerate(self.fingerprintlist):
            # 解析规则字符串
            try:
                rule = item['rule']
                parsed = ast.parse(rule, mode='eval')
                titlename = eval(compile(parsed, '<string>', 'eval'), {'title': title, 'body': body, 'header': header})
                if titlename:
                    self.fingerprintlist[index]['flag'] += 1
                    return item['product']
            except Exception as e:
                print(e, item)

    # 更新指纹文件纹
    def update(self):
        updatefilelist(self.fingerprintlist)


# 命令行参数
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='请输入目标url ', metavar='')
    parser.add_argument('-f', help='请输入需要批量扫描的文件', metavar='')
    parser.add_argument('-t', help='超时时间', metavar='', default=60)
    parser.add_argument('-sem', help='异步sem 数量', metavar='', default=20)
    args = parser.parse_args()
    return args


# 定义banner
def banner():
    print('''
                                __     _ __     ___   
                              / _|   | '  \   (_-<   
                              \__|_  |_|_|_|  /__/_  
                            _|"""""|_|"""""|_|"""""| 
                            "`-0-0-'"`-0-0-'"`-0-0-' 

                            Author：有觉悟的菜鸡顾北''')


# 保存到csv文件
def save_csv(data):
    with open('result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['状态码', '网站名称', "指纹", "网站"])
        try:

            for item in data:
                if item != None:
                    writer.writerow(item)
                else:
                    pass
        except Exception as e:

            print(e)


if __name__ == '__main__':
    ss = readfilelist()
    # print(ss)
