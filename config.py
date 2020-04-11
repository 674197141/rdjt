# -*- coding: utf-8 -*-
'''
@Descripttion: 
@version: 
@Author: 刘宇
@Date: 2019-08-15 18:26:05
@LastEditors: 刘宇
@LastEditTime: 2019-08-27 17:47:36
'''
import os
import logging

# 是否启动Debug模式
import sys

DEBUG = False
# 是否加载权限装饰器
RBAC_DEBUG = True

KETANG_SHIPIN = False

# API 设置
API_HOST = '0.0.0.0'
API_PORT = 5050
if sys.platform == 'win32':
    DATA_SERVER = 'http://localhost:8000'
else:
    DATA_SERVER = 'http://data_api'
# API BASE URL
# API_HOSTNAME = 'http://39.107.75.18:3000'
# 设置SECRET_KEY的值  生成用户令牌用
# SECRET_KEY = os.urandom(24)
# 日志文件存放目录  logs.py使用
LOG_JSON_DATA_PATH = os.path.join('logs', 'json_data')
# 上传文件 目录设置
# UPLOAD_FOLDER = 'app\static\upload_files'  # 文件上传路径
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'upload_files')
# 试卷目录路径
PAPER_PATH = os.path.join(os.getcwd(), 'app', 'static', 'papers')
# 后台用户头像目录
USER_ADMIN_HEAD_IMG_PATH = os.path.join('static', 'admin_user_head_img')
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'upload_files')
# 静态文本文件 目录设置
STATIC_TEXT_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'WEB_STATIC_DATA')
# 院校logo 目录设置
SCHOOL_LOGO_FOLDER = os.path.join('static', 'school_logos')
logging_level = logging.INFO
if sys.platform == 'win32':
    logging_level = logging.DEBUG
# 系统日志设置
LOGGING_SETTING = {'level': logging_level,
                   'format': '[%(asctime)s] [%(levelname)s] [%(module)s] [%(funcName)s] [%(lineno)d] %(message)s',
                   'datefmt': '%Y-%m-%d %H:%M:%S',
                   'filename': os.path.join('logs', 'app.log'),
                   'filemode': 'a',
                   'open_stream_heandler': False,
                   'max_bytes': 5 * 1024 * 1024,
                   'backup_count': 10,
                   }
# rrbac匿名用户权限
RRBAC_ANONYMOUS_ROLE = 'Anon'
# 权限数据库
SQLALCHEMY_POOL_SIZE = 30
SQLALCHEMY_POOL_TIMEOUT = 15
SQLALCHEMY_ECHO = False
SQLALCHEMY_RECORD_QUERIES = True
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://isizy:tvOX09@61.149.7.193:33060/isizy_db?charset=utf8mb4'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://isizy:tvOX09@192.168.1.45:33060/isizy_db?charset=utf8mb4'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://isizy:tvOX09@mysql:3306/isizy_db?charset=utf8mb4'
# 是否启用sql调试
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_TEARDOWN = True
MECHANISM = None
# # 配置多个数据库连接
# SQLALCHEMY_BINDS = {
#     'test': 'mysql+pymysql://isizy:tvOX09@61.149.7.193:33060/test?charset=utf8mb4'
# }


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','xlsx','xls'}  # 允许上传文件类型集合


# 连接池配置
# 1. mincached，最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接
# 2. maxcached，最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接
# 3. maxconnections，最大的连接数，
# 4. blocking，当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，
#              直到当前连接数小于最大连接数，如果这个值是False，会报错，
# 5. maxshared 当连接数达到这个数，新请求的连接会分享已经分配出去的连接
# filmath 连接池配置
ISI_POOL_CONFIG = {
    "mincached": 1,
    "maxcached": 2,
    "maxconnections": 2,
    "blocking": True,
    "maxshared": 15
}
