from clear import PMysql
import put
import time


# 更新代理池
def run():
    print('开始清洗数据库...')
    print('='*100)
    clear_db = PMysql()
    clear_db.main()
    print('=' * 100)
    print('清洗完毕...')
    print('=' * 100)
    print('开始写入新的代理...')
    print('=' * 100)
    put.main()
    print('=' * 100)
    print('写入完毕...')
    print('=' * 100)


if __name__ == '__main__':
    st = time.time()
    run()
    print(f'总耗时：{time.time() - st:.4f}秒')
