# -*- coding: UTF-8 -*-

""""""

import DbConnection
import threading


class DbConnectionPool(object):
    """"""
    def __init__(self):
        """"""
        self.free_con_list = []
        self.host = None
        self.username = None
        self.password = None
        self.db_name = None
        self.port = None

    def set_db_args(self, host, username, password, db_name, port):
        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name
        self.port = port

    def get_connection(self):
        if len(self.free_con_list) > 0:
            return self.free_con_list.pop(0)
        else:
            return self.make_connection()

    def make_connection(self):
        return DbConnection.DbConnection(self.host, self.username, self.password, self.db_name, self.port)

    def free_connection(self, db_con):
        self.free_con_list.append(db_con)


class DbConnectionPoolManager(object):
    """"""
    pool_list = {}
    print 'init pool dict'
    lock = threading.RLock()

    @staticmethod
    def get_db_pool(pool_id, receiver):
        """
        before get the db connection pool , you must make sure that the pool has existed in the pool_list
        Note : should make sure this func is threading security
        :param pool_id:
        :return:
        """
        DbConnectionPoolManager.lock.acquire()
        receiver.set_db_con_pool(DbConnectionPoolManager.pool_list[pool_id])
        DbConnectionPoolManager.lock.release()

    @staticmethod
    def add_con_pool(pool_id, host, username, password, db_name, port):
        """
        it is possible failing to make connection pool
        :param pool_id:
        :return:
        """
        DbConnectionPoolManager.pool_list[pool_id] = DbConnectionPool()
        DbConnectionPoolManager.pool_list[pool_id].set_db_args(host, username, password, db_name, port)

    @staticmethod
    def delete_pool(pool_id):
        DbConnectionPoolManager.pool_list.pop(pool_id)


