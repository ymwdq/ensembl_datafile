# -*- coding: UTF-8 -*-

''

import DbConnection

# class GetSingleDbInstance(object):
#     ''
#     dbInstance = None
#     preHost = None
#     preUser = None
#     prePass = None
#     preDb = None
#     prePort = None
#     def __init__(self):
#         print 'init'
#
#     @staticmethod
#     def getSingleDbInstance(host,userName,password,db,port = 3306):
#         if GetSingleDbInstance.dbInstance == None \
#                 and host != GetSingleDbInstance.preHost\
#                 and userName != GetSingleDbInstance.preUser\
#                 and password != GetSingleDbInstance.prePass\
#                 and db != GetSingleDbInstance.preDb\
#                 and port != GetSingleDbInstance.prePort:
#             GetSingleDbInstance.dbInstance = DBFetcher.DBFetcher(host, userName, password, port)
#         return GetSingleDbInstance.dbInstance
