# -*- coding: utf-8 -*-
### author:chushiyan
### https://github.com/chushiyan/pytube-redis.git
### date:03.19.2019
### vesion:1.0.0

'''
    The program entry
'''
from pytube import YouTube
from pytube import Playlist
import json
import os
import redis
import argparse
import logging
import threading
import time
from queue import Queue

# import other module of this project
from settings import settings
from redisclient.redisclient import RedisClient
from downloader import Downloader


class YouTubeDownloader(object):

    def __init__(self, playlist_url):

        # init a redis client use the
        self.redisClient = RedisClient(host=settings.HOST, port=settings.PORT, password=settings.PASSWORD,
                                       db=settings.DB)

        # the url of the YouTube playlist
        self.playlist_url = playlist_url

        # print(self.playlist_url)

        # create a queue which saves the url of each youtube video
        self.url_queue = Queue()


        logging.basicConfig(level=settings.LOG_LEVEL,
                            format=settings.LOG_FORMAT,
                            datefmt=settings.DATE_FORMAT,
                            filename=settings.LOG_PATH + settings.LOG_FILE
                            )

        # create the directory if it does exist
        if not os.path.exists(settings.FILE_PATH):
            os.mkdir(settings.FILE_PATH)

        self.get_urls_and_save()
        self.add_urls_to_queue()
        self.start_threads()

    def get_urls_and_save(self):
        '''
        parse the playlist with Playlist,
        and save the urls into redis
        '''

        pl = Playlist(self.playlist_url)
        urls = pl.parse_links()
        for url in urls:
            url = 'https://www.youtube.com' + url
            print(url)
            if not self.redisClient.hash_get(self.playlist_url, url):
                self.redisClient.hash_set(self.playlist_url, url, 'False')

    def add_urls_to_queue(self):
        '''
        get urls from redis ,then add to a queue ,
        so the threads can get urls from the queue
        '''
        data = self.redisClient.hash_getall(self.playlist_url)

        for k, v in data.items():
            print(k, v)

        for url, isDownloaded in data.items():
            if isDownloaded == 'False':
                self.url_queue.put(url)

    def start_threads(self):
        '''
        start some threads .
        '''
        downloader_list = []
        for i in range(settings.THREAD_COUNT):
            downloader_list.append(
                Downloader(name='thread-' + str(i), redisClient=self.redisClient, playlist_url=self.playlist_url,
                           url_queue=self.url_queue))

        for downloader in downloader_list:
            downloader.start()
            logging.info('The thread named %s is starting.' % downloader.name)
            print('The thread named %s is starting.' % downloader.name)

        for downloader in downloader_list:
            downloader.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='The program is built for downloading videos from youtube.')
    parser.add_argument('url',
                        help='url of youtube.com.It must be url of video list,not a single video url.')
    args = parser.parse_args()

    print('start...')
    downloader = YouTubeDownloader(args.url)
    print('finish...')
