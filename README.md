# Proxy Pool代理池

## 项目介绍

+ 协程异步抓取代理

+ 多线程检测代理

+ 代理存储在Mysql数据库

+ 对数据库中的代理进行清洗

+ 可以在`paser.py`中扩展可以爬取代理的网站

+ ~~在爬虫应用过程中发现，极大部分代理无法访问https网站，访问http网站没有太大问题，推测是由于aiohttp在使用代理时只支持http类型代理导致筛选机制出现问题，目前计划使用gevent + requests代替（不过我觉得筛选更加严格后能用的ip更少了。。免费的质量还是不能强求。。）~~

+ 免费代理的质量实在是太差，能用的太少太少太少少少少少了，有条件的还是建议使用付费代理

  

## 运行环境

+ Python 3.6以上

+ Mysql



## 安装依赖

`pip install -r requirements.txt`



## 配置数据库

`conf.py`文件中：

```python
HOST = '127.0.0.1'    # Mysql Host
PORT = 3306           # PORT
USER = 'root'         # 用户名
PASSWORD = 'password' # 密码
DB = 'db_name'        # 数据库名
TABLE = 'table_name'  # 表名
ROW = 'row_name'      # 代理所在字段名
```

ps：数据库代理所在字段建议设置为主键，避免代理重复入库

## 清洗数据库

`python main.py`



## 使用API获取代理

+ `python webapi.py`        (使用时请务必保持开启状态)

+ 访问`http://127.0.0.1:5000/`进入主页

+ 点击`"随机获取代理"`或访问`http://127.0.0.1:5000/proxy`可随机获取一条代理，刷新页面可重新获取代理

+ 点击`"代理数量"`或访问`http://127.0.0.1:5000/count`可以查询数据库中代理数量

+ 爬虫中代理的使用:

  ```python
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
  ```

  





