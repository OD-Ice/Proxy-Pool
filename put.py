import asyncio
import aiomysql
from check import Check
from conf import HOST, PORT, USER, PASSWORD, DB, TABLE, ROW
from paser import Ip3366, Xici, Kuai, Jiang, Qiyun


# 写入新的代理
class Putproxy:
    def __init__(self, proxies):
        self.host = HOST
        self.port = PORT
        self.user = USER
        self.password = PASSWORD
        self.db = DB
        self.table = TABLE
        self.row = ROW
        self.proxies = proxies

    async def put_proxy(self, proxy, pool):
        sql_put = f'INSERT INTO {self.table} VALUES("{proxy}")'
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(sql_put)
                    print(f'写入{proxy}')
                    await conn.commit()
                except Exception:
                    print(f'代理重复：{proxy}')
                    await conn.rollback()

    async def connect_pool(self, loop):
        # 创建连接池
        pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            loop=loop,
        )

        for proxy in self.proxies:
            await self.put_proxy(proxy, pool)

        # 连接池不用时
        pool.close()
        # 避免池中连接用完，等待连接断开
        await pool.wait_closed()

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect_pool(loop))


def main():
    proxies_list = []

    ip3366 = Ip3366()
    xici = Xici()
    kuai = Kuai()
    jiang = Jiang()
    qiyun = Qiyun()

    proxies_list.extend(ip3366.get_proxy())
    proxies_list.extend(xici.get_proxy())
    proxies_list.extend(kuai.get_proxy())
    proxies_list.extend(jiang.get_proxy())
    proxies_list.extend(qiyun.get_proxy())

    # 检测代理
    usable = Check(proxies_list)
    usable_proxies = usable.usable_proxies
    print(usable_proxies)

    put = Putproxy(usable_proxies)
    put.run()


if __name__ == '__main__':
    main()
