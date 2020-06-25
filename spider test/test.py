import requests
from lxml import etree


# 尝试使用代理池获取代理进行爬虫
class Spider:
    def __init__(self):
        self.url = 'https://www.bilibili.com'
        self.headers = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)'}
        self._proxy = ''

    # 获取代理
    @property
    def proxy(self):
        url = 'http://127.0.0.1:5000/proxy'
        res = requests.get(url)
        self._proxy = res.text
        return self._proxy

    # 爬虫
    def get_page(self):
        proxies = {'https': self.proxy, 'http': self.proxy}
        res = requests.get(self.url, headers=self.headers, proxies=proxies, timeout=3)
        tree = etree.HTML(res.content.decode())
        title = tree.xpath('/html/head/title/text()')[0]
        print(title)


if __name__ == '__main__':
    spider = Spider()
    spider.get_page()
