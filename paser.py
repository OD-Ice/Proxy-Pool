from spider import Downloader
import bs4
import time
from check import Check


# 针对不同的网站进行分析
# 云代理
class Ip3366:
    url = 'http://www.ip3366.net/free/?stype=1&page={}'

    def get_proxy(self, pages=7):
        urls = []
        proxies = []
        for i in range(1, pages + 1):
            urls.append(self.url.format(i))
        downloader = Downloader(urls)
        soups = downloader.soups
        for soup in soups:
            proxy_list = soup.find('tbody').find_all('tr')
            for each in proxy_list:
                ip = each.find_all('td')[0].get_text()
                port = each.find_all('td')[1].get_text()
                proxy = ':'.join([ip, port])
                proxies.append(proxy)
        return proxies


# 西刺代理
class Xici:
    url = 'https://www.xicidaili.com/nn/{}'

    def get_proxy(self, pages=2):
        urls = []
        proxies = []
        for i in range(1, pages + 1):
            urls.append(self.url.format(i))
        downloader = Downloader(urls)
        soups = downloader.soups
        for soup in soups:
            proxy_list = soup.find(name='table', id='ip_list').find_all(name='tr', class_='odd')
            for each in proxy_list:
                ip = each.find_all('td')[1].get_text()
                port = each.find_all('td')[2].get_text()
                proxy = ':'.join([ip, port])
                proxies.append(proxy)
        return proxies


# 快代理
class Kuai:
    url = 'https://www.kuaidaili.com/free/inha/{}/'

    def get_proxy(self, pages=5):
        proxies = []
        n = 1
        while n <= pages:
            urls = [self.url.format(n)]
            downloader = Downloader(urls)
            soups = downloader.soups
            for soup in soups:
                proxy_list = soup.find('tbody')
                proxy_list = proxy_list.find_all('tr')
                for each in proxy_list:
                    ip = each.find_all('td')[0].get_text()
                    port = each.find_all('td')[1].get_text()
                    proxy = ':'.join([ip, port])
                    proxies.append(proxy)
            # 这个网站访问过快就没有数据，快代理快不起来了-_-!
            time.sleep(1)
            n += 1
        return proxies


# 不知道是什么的代理
class Jiang:
    url = 'https://ip.jiangxianli.com/?page={}&anonymity=2'

    def get_proxy(self, pages=11):
        proxies = []
        n = 1
        while n <= pages:
            urls = [self.url.format(n)]
            downloader = Downloader(urls)
            soups = downloader.soups
            for soup in soups:
                proxy_list = soup.find('tbody')
                proxy_list = proxy_list.find_all('tr')
                for each in proxy_list:
                    ip = each.find_all('td')[0].get_text()
                    port = each.find_all('td')[1].get_text()
                    proxy = ':'.join([ip, port])
                    proxies.append(proxy)
            # 这个网站访问过快就没有数据
            time.sleep(1)
            n += 1
        return proxies


# 齐云代理
class Qiyun:
    url = 'https://www.7yip.cn/free/?action=china&page={}'

    def get_proxy(self, pages=7):
        urls = []
        proxies = []
        for i in range(1, pages + 1):
            urls.append(self.url.format(i))
        downloader = Downloader(urls)
        soups = downloader.soups
        for soup in soups:
            proxy_list = soup.find(name='tbody').find_all(name='tr')
            for each in proxy_list:
                ip = each.find_all('td')[0].get_text()
                port = each.find_all('td')[1].get_text()
                proxy = ':'.join([ip, port])
                proxies.append(proxy)
        return proxies
