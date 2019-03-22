# pytube-redis
## 概述 Description
+ 这是一个用于下载youtube视频列表的完整项目
+ This is a completed project for downloading youtube video playlist.
+ 基于pytube模块
+ It is based on the pytube module.

+ This project is just encapsulating the pytube module.

***
## 为什么不直接使用pytube下载? Why not just use pytube to download?
+ In some cases,I use pytube to download youtube video playlist,I have to interrupt the program .
+ When I restart the program ,pytube will dowmload all videos even they are already dowmloaded.
+ So ,I use redis to record the urls of the playlist as keys.If the video is downloaded,modify the key's
value to True. 
+ 使用redis去重，保证中断下载之后重新下载不会重复下载。



## 用法 Usage
+ 首先安装pytube、redis模块
+ 1 Fisrt of all,install the pytube module ,the python redis module
```
pip install pytube
pip install redis
```
***
+ 修改本项目中的settings.py文件，指定自己的配置
+ 2 Modify the settings.py of this project to specify your own configuration

```
#(1) The redis database configuration.
HOST = "localhost"
PORT = 6379
PASSWORD = "replace with your database's password"
DB = 0

#(2)the path where you want to save the videos
FILE_PATH = './video'

#(3)logging
LOG_LEVEL = 'DEBUG'
LOG_PATH = './'
LOG_FILE = '/pytube-redis.log'

LOG_FORMAT = "%(asctime)s %(name)s %(levelname)s %(pathname)s %(message)s "
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '

#(4)specify the numbers of download thread
THREAD_COUNT = 3
```
***
+ 执行run.py
+ 3 execute the run.py
 like this :(specify the url of youtube playlist)
 ```
python run.py "https://www.youtube.com/watch?v=lEORlC3WIJU&list=PLNJMtLp9N3esMNkSwwZM0qY0qCCWvcmIc"
```




