# Proxy Pool代理池

## 项目介绍

+ 多线程抓取代理

+ 协程异步检测代理

+ 代理存储在Mysql数据库

+ 对数据库中的代理进行清洗

+ 目前版本存在重大bug：

  + 由于是从免费代理中进行抓取，可用的代理很少

  + 在爬虫应用过程中发现，极大部分代理无法访问https网站，访问http网站没有太大问题，

    推测是由于aiohttp在使用代理时只支持http类型代理导致筛选机制出现问题，目前计划使用

    gevent + requests代替