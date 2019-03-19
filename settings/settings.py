# -*- coding: utf-8 -*-
### author:chushiyan
### https://github.com/chushiyan/pytube-redis.git
### date:03.19.2019
### vesion:1.0.0

# 1、The redis database configuration.
HOST = "localhost"
PORT = 6379
PASSWORD = "replace with your database's password"
DB = 0

# 2、the path where you want to save the videos
FILE_PATH = './video'

# 3、logging
LOG_LEVEL = 'DEBUG'
LOG_PATH = './'
LOG_FILE = '/pytube-redis.log'

LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '

# 4、specify the numbers of download thread
THREAD_COUNT = 3
