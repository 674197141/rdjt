# -*- coding: utf-8 -*-
import logging.handlers
import os
import sys
from datetime import datetime
from decimal import Decimal
import pymysql
from flask import Flask
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import numpy as np
import config


def get_dict_conn(db_name="model"):
    try:
        if db_name != 'model':
            return pymysql.connect(host=app.config['ISI_MYSQL_CONFIG']["host"],
                                   port=app.config['ISI_MYSQL_CONFIG']["port"],
                                   user=app.config['ISI_MYSQL_CONFIG']["user"],
                                   password=app.config['ISI_MYSQL_CONFIG']["passwd"],
                                   db=db_name, charset=app.config['ISI_MYSQL_CONFIG']["charset"],
                                   cursorclass=pymysql.cursors.DictCursor)
        else:
            return pymysql.connect(host=app.config['MODEL_MYSQL_CONFIG']["host"],
                                   port=app.config['MODEL_MYSQL_CONFIG']["port"],
                                   user=app.config['MODEL_MYSQL_CONFIG']["user"],
                                   password=app.config['MODEL_MYSQL_CONFIG']["passwd"],
                                   db=db_name, charset=app.config['MODEL_MYSQL_CONFIG']["charset"],
                                   cursorclass=pymysql.cursors.DictCursor)

    except Exception as e:
        print(e)
        return None


app = Flask(__name__)


Compress(app)
app.config.from_object(config)
print('===========加载配置文件============')
# 初始化数据库连接池
# 主数据库连接池

db = SQLAlchemy(app, engine_options={
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "pool_use_lifo": True,
    "max_overflow": 0})
print("==========连接数据库============")
BaseDb = automap_base()
BaseDb.prepare(db.get_engine())


class Base_DB_Model(db.Model):
    __abstract__ = True

    @property
    def dc(self) -> dict:
        return self.to_dc()

    def to_dc(self) -> dict:
        result = {}
        for key in list(self.__mapper__.c.keys()):
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 准备替换掉pool的，一个服务里两个连接池太多了
def get_conn():
    engine = db.get_engine()
    return engine.raw_connection()


Session_factory = sessionmaker(bind=db.get_engine())
Session = scoped_session(Session_factory)


def get_session():
    session = Session()
    return session

# r.flushall()  # 服务启动的时候清空redis

# 初始化系统日志
print("==========初始化系统日志==========")
formatter = logging.Formatter(fmt=app.config['LOGGING_SETTING']['format'],
                              datefmt=app.config['LOGGING_SETTING']['datefmt'])
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=app.config['LOGGING_SETTING']['level'],
                    format=app.config['LOGGING_SETTING']['format'],
                    datefmt=app.config['LOGGING_SETTING']['datefmt'],
                    # filename=app.config['LOGGING_SETTING']['filename'],
                    # filemode=app.config['LOGGING_SETTING']['filemode']
                    )
Logger = logging.getLogger('app')
# Logger = app.logger
if not sys.platform == 'win32':
    log_file = os.path.join('logs', 'app.log')
    handler = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight', 1)
    handler.suffix = "%Y%m%d.log"  # 设置 切分后日志文件名的时间格式 默认 filename+"." + suffix
    handler.setFormatter(formatter)
    handler.setLevel(app.config['LOGGING_SETTING']['level'])
    Logger.addHandler(handler)
    try:
        for par in r.hgetall("job_cache"):
            r.hdel("job_cache", par)
    except Exception as e:
        Logger.error(e)
else:
    log_file = os.path.join('logs', 'app.log')
    handler = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight', 1)
    handler.suffix = "%Y%m%d.log"  # 设置 切分后日志文件名的时间格式 默认 filename+"." + suffix
    handler.setFormatter(formatter)
    handler.setLevel(app.config['LOGGING_SETTING']['level'])
    app.logger.addHandler(handler)

import json


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, int):
            return str(o)
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, bytes):
            o.decode('utf-8')
            return str(o, encoding='utf-8')
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, o)


app.json_encoder = JSONEncoder

from app import views

Logger.info("创建数据库")
db.create_all()


Logger.info("------------启动成功------------")
