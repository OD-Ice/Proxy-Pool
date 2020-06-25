import asyncio
import aiomysql
from check import Check
from conf import HOST, PORT, USER, PASSWORD, DB, TABLE, ROW


# 清洗数据库中代理
class PMysql:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.user = USER
        self.password = PASSWORD
        self.db = DB
        self.table = TABLE
        self.row = ROW

    async def check_proxy(self, pool):
        sql_get = f"SELECT {self.row} FROM {self.table}"
        # 从空闲池获取连接的协程。根据需要创建新连接，并且池的大小小于maxsize
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql_get)
                # 对提取出的代理进行检测
                proxies_get = [each[0] for each in await cursor.fetchall()]
        return proxies_get

    async def del_proxy(self, disable_proxy, pool):
        sql_del = f"DELETE FROM {self.table} WHERE {self.row}='{disable_proxy}'"
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(sql_del)
                await conn.commit()
                print(f'删除{disable_proxy}')

    async def run(self, loop):
        # 创建连接池
        pool = await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            loop=loop,
        )

        proxies_get = await self.check_proxy(pool)

        check_proxy = Check(proxies_get)
        # 获得不能使用的proxies
        disable_proxies = check_proxy.disable_proxies

        for each in disable_proxies:
            await self.del_proxy(each, pool)

        # 连接池不用时
        pool.close()
        # 避免池中连接用完，等待连接断开
        await pool.wait_closed()

    def main(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run(loop))


if __name__ == '__main__':
    a = PMysql()
    a.main()
