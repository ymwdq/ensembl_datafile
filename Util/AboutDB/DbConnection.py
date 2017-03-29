# -*- coding: UTF-8 -*-

""""""

import MySQLdb


class DbConnection(object):
    """"""
    def __init__(self, host, username, password, db, port=3306):
        self.has_query_success = True
        self.has_connected_success = True

        try:
            self.db_con = MySQLdb.connect(host=host, user=username, passwd=password, db=db, port=port, charset='utf8')
            self.cursor = self.db_con.cursor()
            print('db connect successfully')
        except Exception as exc:
            print('db connection error')
            print(exc)
            self.close_cursor()
            self.close_con()
            self.has_connected_success = False

    def set_autocommit(self, commit_code=1):
        self.db_con.autocommit(commit_code)

    def execute_query(self, query_string):
        print('sql', query_string)
        r = None
        try:
            r = self.cursor.execute(query_string)
        except Exception as exc:
            print('query error')
            print(exc)
            self.has_query_success = False
        finally:
            return r

    def set_con(self, host, username, password, db, port):
        self.db_con = MySQLdb.connect(host=host, user=username, passwd=password, db=db, port=port)
        self.cursor = self.db_con.cursor()

    def close_con(self):
        self.db_con.close()

    def close_cursor(self):
        self.cursor.close()

    def get_res(self):
        return self.cursor.fetchall()

    def has_connected(self):
        return self.has_connected_success

    def has_query(self):
        return self.has_query_success
