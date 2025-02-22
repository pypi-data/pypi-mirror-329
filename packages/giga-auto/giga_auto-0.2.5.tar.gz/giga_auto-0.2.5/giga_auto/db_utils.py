import os
import cx_Oracle
import pymssql
import pymysql

from giga_auto.logger import db_log


class DBUtils():

    def __init__(self, db_config,db_type='mysql'):
        self.db_config = db_config
        self.conn = None
        self.cursor=None
        self.db_type = db_type

    def _connect(self):
        if self.db_type == 'sqlserver':
            self.sqlserver_connection()
        elif self.db_type == 'mysql':
            self.mysql_connect()
        self.cursor = self.conn.cursor()

    def sqlserver_connection(self):
        self.conn = pymssql.connect(
            server=self.db_config["db_host"],
            port=int(self.db_config["db_port"]),
            user=self.db_config["db_user"],
            password=self.db_config["db_password"],
            database=self.db_config["db_name"]
        )

    def mysql_connect(self):
        self.conn = pymysql.connect(
            host=self.db_config["db_host"],
            port=int(self.db_config["db_port"]),
            user=self.db_config["db_user"],
            password=self.db_config["db_password"],
            database=self.db_config["db_name"],
            charset=self.db_config["db_charset"]
        )
        return self.conn

    def get_cursor(self, dict_cursor):
        if self.db_type == 'mysql':
            cursor = self.conn.cursor(pymysql.cursors.DictCursor) if dict_cursor else self.conn.cursor()
        elif self.db_type == 'sqlserver':
            cursor = self.conn.cursor(
                as_dict=True) if dict_cursor else self.conn.cursor()  # SQL Server supports `as_dict`
        return cursor

    @db_log
    def _execute(self, sql, params=None):
        """

        :param sql:
        :param params: [()] or [[]]
        :return:
        """
        many = params and len(params) > 1
        if many:
            self.cursor.executemany(sql, params)
        else:
            self.cursor.execute(sql, params[0] if params else None)
        self.conn.commit()
        return self.cursor.rowcount

    @db_log
    def _fetchone(self, sql, args=None, dict_cursor=True):
        cursor = self.get_cursor(dict_cursor)
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        return cursor.fetchone()

    @db_log
    def _fetchall(self, sql, args=None, dict_cursor=True):
        cursor = self.get_cursor(dict_cursor)
        if args:
            cursor.execute(sql, args)
        else:
            cursor.execute(sql)
        return cursor.fetchall()