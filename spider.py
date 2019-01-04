import re
import time
import urllib.request

import config as conf


class MySpider:

    def __init__(self, base_url=conf.BASE_URL, header=conf.FAKE_HEADER, start_page=1):
        self.base_url = base_url
        self.start_page = start_page
        self.headers = header

    def fetch_book_name_list(self):
        while self.start_page < 6: #爬去前6页书籍的下载链接，可自己设置，若设置为 while True则爬取所有页的书籍
            try:
                req = urllib.request.Request(
                    self.base_url + '/page/{}'.format(self.start_page), headers=self.headers)
                html = urllib.request.urlopen(req)
                doc = html.read().decode('utf8')
                alist = list(set(re.findall(conf.BOOK_LINK_PATTERN, doc))) # 每页书籍的跳转链接
                print(alist)
                print('\npage {}\n'.format(self.start_page))
                time.sleep(10)
                self.start_page += 1
                self.fetch_download_link(alist)
            except urllib.error.HTTPError as err:
                print(err.msg)
                break

    def fetch_download_link(self, alist):
        fres = open('result.txt', 'a')
        for item in alist:
            req = urllib.request.Request(item,headers=self.headers)
            html = urllib.request.urlopen(req)
            doc = html.read().decode('utf8')
            try:
                url = re.findall(conf.DOWNLOAD_LINK_PATTERN, doc)[0] # 从书的详情页面中，找到下载链接
                print('{}'.format(url))
                fres.write(url + '\n')
            except IndexError:
                ferr = open('error.txt', 'a')
                ferr.write(item + '\n')
                ferr.close
            time.sleep(3)
        fres.close()

    def run(self):
        self.fetch_book_name_list()


if __name__ == '__main__':
    mc = MySpider()
    mc.run()
