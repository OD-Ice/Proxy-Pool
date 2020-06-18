import requests
from bs4 import BeautifulSoup
import re
from multiprocessing.dummy import Pool
import time
import asyncio
import aiohttp
import pymysql
# 数据库连接池模块
from DBUtils.PooledDB import PooledDB
# 忽略警告信息
import warnings
warnings.filterwarnings("ignore")


class Proxy:
    def __init__(self):
        # 创建数据库连接池
        self.user = input('MySql数据库用户名：')
        self.passwd = input('MySql数据库密码：')
        self.database = input('代理所在数据库：')
        self.pool = self.mysql_connection()

        self.proxies = []
        self.urls = []
        self.can_list = []
        # 只取前五页，后面的太旧了
        for i in range(1, 6):
            self.urls.append(f'http://www.ip3366.net/free/?stype=1&page={i}')
            self.urls.append(f'https://www.xicidaili.com/nn/{i}')
            self.urls.append(f'https://www.kuaidaili.com/free/inha/{i}/')
            self.urls.append(f'https://ip.jiangxianli.com/?page={i}&anonymity=2')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'
        }

    # 创建数据库连接池
    def mysql_connection(self):
        # 最大连接数
        maxconnections = 15
        pool = PooledDB(
            pymysql,
            maxconnections,
            host='127.0.0.1',
            port=3306,
            user=self.user,
            passwd=self.passwd,
            db=self.database,
            use_unicode=True
        )
        return pool

    def get_res(self, url):
        res = requests.get(url, headers=self.headers)
        return res.content

    @staticmethod
    def get_ip(content):
        proxies = []
        soup = BeautifulSoup(content, 'lxml')
        ip_nums = soup.find_all(text=re.compile(r'\d+\.\d+\.\d+\.\d+'))
        for ip_num in ip_nums:
            # 通过parent获取标签，text和get_text()获得的结果一样
            # 用两次next_sibling，两标签中间会出现空白标签，原因未知
            port = ip_num.parent.next_sibling.next_sibling.text
            if port == '高匿' or port == '高匿名':
                port = ip_num.parent.next_sibling.text
            proxy = ':'.join([ip_num, port])
            proxies.append(proxy)
        return proxies

    async def check_ip(self, proxy, is_clear=False):
        # 超时时间要用ClientTimeout(total=3)设置, session则可以直接写int类型
        # timeout = aiohttp.ClientTimeout(total=3)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url='http://www.baidu.com', headers=self.headers, proxy=f'http://{proxy}',
                                       timeout=2, verify_ssl=False) as res:
                    if res.status == 200:
                        print(f'{proxy} : 可以使用!')
                        if not is_clear:
                            self.can_list.append(proxy)
                    else:
                        print(f'{proxy} : 不可使用!')
        except Exception:
            print(f'{proxy} : 不可使用!')
            if is_clear:
                return proxy

    def save(self, proxy):
        # 利用连接池创建连接
        conn = self.pool.connection()
        cursor = conn.cursor()
        # 注意pymysql语法的使用规则
        sql = f'INSERT INTO ip(proxies) VALUES(%s)'
        try:
            cursor.execute(sql, proxy)
            conn.commit()
            print(f'写入{proxy}')
        except Exception as e:
            print(f'代理重复：{proxy}', e)
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def del_ip(self, t):
        # 不要忘了()
        if t.result():
            conn = self.pool.connection()
            cursor = conn.cursor()
            sql = f'DELETE FROM ip WHERE proxies=%s'
            try:
                cursor.execute(sql, t.result())
                conn.commit()
                print(f'删除{t.result()}')
            except Exception:
                conn.rollback()
            finally:
                cursor.close()
                conn.close()

    def clear_ip(self):
        conn = self.pool.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 括号内参数使数据以字典形式显示，可以看到键
        sql = 'SELECT * FROM ip'
        cursor.execute('CREATE TABLE IF NOT EXISTS ip(id INT PRIMARY KEY AUTO_INCREMENT, proxies VARCHAR(20) UNIQUE)')
        cursor.execute(sql)

        # 建立协程任务列表
        tasks = []
        for each in cursor.fetchall():
            task = asyncio.ensure_future(self.check_ip(each['proxies'], is_clear=True))
            task.add_done_callback(self.del_ip)
            tasks.append(task)
        if tasks:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
        cursor.close()
        conn.close()

    def main(self):
        # 建立线程池
        pool = Pool(8)
        # 访问网站
        contents = pool.map(self.get_res, self.urls)
        # 获取ip
        proxies = pool.map(self.get_ip, contents)
        for each in proxies:
            self.proxies.extend(each)

        # 建立协程任务列表
        tasks = []
        for each in self.proxies:
            task = asyncio.ensure_future(self.check_ip(each))
            tasks.append(task)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        # 此时已获取可用ip
        pool.map(self.save, self.can_list)

    def count(self):
        conn = self.pool.connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = [
            'alter table ip drop id',
            'alter table ip add id int not null primary key auto_increment first',
            'SELECT COUNT(*) FROM ip'
            ]
        for each in sql:
            cursor.execute(each)
        print(f'Proxy总数：{cursor.fetchall()[0]["COUNT(*)"]}')
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    start_time = time.time()
    proxy_item = Proxy()
    print('=' * 100)
    print('开始清洗代理池...')
    print('=' * 100)
    proxy_item.clear_ip()
    print('='*100)
    print('导入新的代理...')
    proxy_item.main()
    print('=' * 100)
    proxy_item.count()
    print('=' * 100)
    print('导入完成！\n总耗时:', time.time() - start_time)
