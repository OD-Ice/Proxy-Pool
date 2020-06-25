from flask import Flask, render_template
import random
import pymysql
from conf import HOST, PORT, USER, PASSWORD, DB, TABLE, ROW

app = Flask(__name__)


# 连接数据库
def connection():
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        passwd=PASSWORD,
        db=DB
    )
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/proxy')
def get_proxy():
    conn = connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f'SELECT {ROW} FROM {TABLE} ORDER BY RAND() LIMIT 1'
    cursor.execute(sql)
    proxy = cursor.fetchone()
    cursor.close()
    conn.close()
    return proxy['proxy']


@app.route('/count')
def get_count():
    conn = connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = f'SELECT COUNT(*) FROM {TABLE}'
    cursor.execute(sql)
    count = cursor.fetchone()
    cursor.close()
    conn.close()
    return f'数据库中共有{count["COUNT(*)"]}条代理'

if __name__ == '__main__':
    app.run()
