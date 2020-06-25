import requests
from headers_pool import User_Agent
import random
import threading
from queue import Queue
import time


# 检测代理
class Check:
    def __init__(self, proxies):
        # 创建代理队列
        self.proxies = Queue()
        for each in proxies:
            self.proxies.put(each)
        self.url = 'https://www.baidu.com'
        self.user_agents = User_Agent()
        self.user_agent = random.choice(self.user_agents.user_agents)
        self.headers = {'User-Agent': self.user_agent}
        self._usable_proxies = []
        self._disable_proxies = []

    def check_proxy(self):
        while True:
            proxy = self.proxies.get()
            proxies = {'https': proxy, 'http': proxy}
            try:
                res = requests.get(self.url, headers=self.headers, proxies=proxies, timeout=5)
                if res.status_code == 200:
                    self._usable_proxies.append(proxy)
                    print(f'{proxy}可用！')
                else:
                    print(f'{proxy}不可用！')
                    self._disable_proxies.append(proxy)
            except Exception:
                print(f'{proxy}不可用！')
                self._disable_proxies.append(proxy)
            self.proxies.task_done()

    def run(self):  # 实现主要逻辑
        thread_list = []
        for i in range(8):
            t_parse = threading.Thread(target=self.check_proxy)
            thread_list.append(t_parse)
        for thread in thread_list:
            # 设置为守护线程，主线程结束，子线程结束
            thread.setDaemon(True)
            thread.start()
        # 让主线程阻塞，等待队列任务完成
        self.proxies.join()
        print('检测结束！')

    @property
    def usable_proxies(self):
        self.run()
        return self._usable_proxies

    @property
    def disable_proxies(self):
        self.run()
        return self._disable_proxies
