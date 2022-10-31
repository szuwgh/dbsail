import click
import psycopg2
import pymysql
from pymysql.cursors import Cursor
from pymysql.connections import Connection
import os

info = 'rWbhSHMi42ItE5GnqLgAQAHkb5PUsT1m7t8i3JzAteElBRqqDbzxKxwjUMi2aFM1VdjHLat4HV8KCqZQXD7Odi9hEWfbVowWjpWvKnxP8aRf93fdLBniNHDGQlVrYUzP9HbBNFthgapdKlbn78NwiyZkekKesTVhpHnHwDpAS71B7Lzrkz58pToEOgzWTEn8xvGeQirDFr7VFkQHev4tdiN4r8aID8n9Aqjf5QdvDHSIBdPy4VtpqSgWIF5XjfN'
one_raw_size = 1  # 1KB
v = '0.1'
mysql_insert_sql = 'insert into test1 (FIRST_NAME,LAST_NAME, AGE, SEX, INFO, INCOME) values(%s,%s,%s,%s,%s,%s)'
mysql_raw_data = ('Mac', 'Mohan', 20, 'M', info, 2000.11)


def exit():
    os._exit(0)


def size_to_int(size: str):
    d = size[-1]
    try:
        i = int(size[:-1])
    except Exception as e:
        print('size format error , check if it is in 1K, 1M, 1G format:', e)
        exit()
    s = 0
    if d == 'K' or d == 'k':
        s = i
    elif d == 'M' or d == 'm':
        s = i * 1024  # KB
    elif d == 'G' or d == 'g':
        s = i * 1024 * 1024
    return s


class Mysql:
    db: Connection
    cur: Cursor

    def __init__(self, host, user, port, password):
        try:
            self.db = pymysql.connect(
                host=host,
                user=user,
                port=port,
                password=password,
            )
            self.cur = self.db.cursor()
        except Exception as e:
            print('connect mysql fail:', e)
            exit()
        print("connect mysql success", "{}:{}".format(host, port))

    # 创建数据库
    def create_data_base(self, data_base):
        sql = "CREATE DATABASE if not exists {}".format(data_base)
        self.execute(sql)
        print("create data base %s" % data_base)

    # 删除数据库
    def delete_data_base(self, data_base):
        sql = "DROP DATABASE {}".format(data_base)
        self.execute(sql)
        print("drop data base %s" % data_base)

    # 使用哪个数据库
    def use(self, data_base):
        sql = "use {}".format(data_base)
        self.execute(sql)
        print("use data base %s" % data_base)

    # 创建数据库表
    def create_table(self):
        sql = """CREATE TABLE if not exists test1 (
         id int(11) primary key NOT NULL AUTO_INCREMENT,
         FIRST_NAME  CHAR(255) NOT NULL,
         LAST_NAME  CHAR(255),
         AGE int(11),  
         SEX CHAR(247),
         INFO CHAR(255),
         INCOME FLOAT )"""
        self.execute(sql)
        print("create table test1\n")

    # 关闭数据库
    def close(self):
        self.db.close()

    # 插入数据
    def insert_data(self, batch, count, size):
        s = int(size_to_int(size) / one_raw_size)
        if count == 0:
            count = s
        import time
        from time import strftime
        from time import gmtime
        ticks1 = time.time()
        from progress.bar import ChargingBar
        q = int(count / batch)
        r = count % batch
        bar = ChargingBar('Processing',
                          max=q + 1,
                          suffix='%(percent)d%%',
                          width=64)
        for _ in range(0, q):
            values = []
            for _ in range(0, batch):
                values.append(mysql_raw_data)
            self.executemany(mysql_insert_sql, values)
            bar.next()
        if r > 0:
            values = []
            for _ in range(0, r):
                values.append(mysql_raw_data)
            self.executemany(mysql_insert_sql, values)
        bar.next()
        bar.finish()
        ticks2 = time.time()
        st = strftime("%H:%M:%S", gmtime(ticks2 - ticks1))
        print("finish insert %s rows data, usage time %s" % (count, st))

    def executemany(self, sql, values):
        try:
            # 执行sql语句
            self.cur.executemany(sql, values)
            # 提交到数据库执行

            self.db.commit()

        except Exception as e:
            # 如果发生错误则回滚
            self.db.rollback()
            print('execute sql fail:', sql, e)
            self.db.close
            exit()

    def execute(self, sql):
        try:
            # 执行sql语句
            self.cur.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            # 如果发生错误则回滚
            self.db.rollback()
            print('execute sql fail:', sql, e)
            self.db.close
            exit()


@click.group()  #将main函数装饰成一个group对象
def main():
    print(
        '\nThis tool is used to connect to mysql or postgresql and insert data of customizable size, power by szuwgh'
    )
    print('''
      ___           ___           ___           ___                       ___ 
     /\  \         /\  \         /\  \         /\  \          ___        /\__\\
    /::\  \       /::\  \       /::\  \       /::\  \        /\  \      /:/  /
   /:/\:\  \     /:/\:\  \     /:/\ \  \     /:/\:\  \       \:\  \    /:/  / 
  /:/  \:\__\   /::\~\:\__\   _\:\~\ \  \   /::\~\:\  \      /::\__\  /:/  /  
 /:/__/ \:|__| /:/\:\ \:|__| /\ \:\ \ \__\ /:/\:\ \:\__\  __/:/\/__/ /:/__/   
 \:\  \ /:/  / \:\~\:\/:/  / \:\ \:\ \/__/ \/__\:\/:/  / /\/:/  /    \:\  \   
  \:\  /:/  /   \:\ \::/  /   \:\ \:\__\        \::/  /  \::/__/      \:\  \  
   \:\/:/  /     \:\/:/  /     \:\/:/  /        /:/  /    \:\__\       \:\  \ 
    \__/__/       \__/__/       \__/__/        /_/__/      \/__/        \_\__\\
    ''')
    pass


@click.group(invoke_without_command=True)  #将下面函数装饰成命令
@click.option('--host',
              '-h',
              default='localhost',
              type=str,
              help='mysql host address')
@click.option('--user',
              '-u',
              default='root',
              type=str,
              help='mysql user account')
@click.option('--port', '-P', default=3306, type=int, help='mysql port')
@click.option('--password',
              '-p',
              default='xxx',
              type=str,
              help='mysql passport')
@click.option('--database',
              '-d',
              default='kmetest',
              type=str,
              help='mysql database')
@click.option('--batch',
              '-b',
              default=10,
              type=int,
              help='batch insert count,ex: 10')
@click.option('--count',
              '-c',
              default=0,
              type=int,
              help='insert count ex: 1000')
@click.option('--size',
              '-s',
              default='10M',
              type=str,
              help='insert size ex: 1K,1M,1G')
@click.pass_context
def mysql(ctx, host, user, port, password, database, batch, count, size):
    if ctx.invoked_subcommand is None:
        print('running dbsail mysql model\n')
        db = Mysql(host=host, user=user, port=port, password=password)
        db.create_data_base(database)
        db.use(database)
        db.create_table()
        db.insert_data(batch, count, size)
        db.close()
    pass


@click.command(name='clean')
@click.option('--host',
              '-h',
              default='localhost',
              type=str,
              help='mysql host address')
@click.option('--user',
              '-u',
              default='root',
              type=str,
              help='mysql user account')
@click.option('--port', '-P', default=3306, type=int, help='mysql port')
@click.option('--password',
              '-p',
              default='xxx',
              type=str,
              help='mysql passport')
@click.option('--database',
              '-d',
              default='kmetest',
              type=str,
              help='mysql database')  #mysql clean 子命令
def mysql_clean(
    host,
    user,
    port,
    password,
    database,
):
    print("use mysql clean")
    db = Mysql(host=host, user=user, port=port, password=password)
    db.delete_data_base(database)
    db.close()


@click.group(invoke_without_command=True)  #将下面函数装饰成命令0
@click.option('--name', '--a', default='ZJW', type=str, help='skfjkskfs name.')
@click.pass_context
def pg(ctx, name):
    if ctx.invoked_subcommand is None:
        print("xx")
    pass


@click.command(name='clean')
@click.option('--debug', default=False)
def pg_clean(debug):
    print("use pg clean")


@click.command(name='version')
def version():
    print("dbsail version", v, "linux/amd64")


main.add_command(mysql)
main.add_command(pg)
main.add_command(version)
mysql.add_command(mysql_clean)
pg.add_command(pg_clean)

if __name__ == '__main__':
    main()
