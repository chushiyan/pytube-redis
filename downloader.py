# -*- coding: utf-8 -*-
### author:chushiyan
### https://github.com/chushiyan/pytube-redis.git
### date:03.19.2019
### vesion:1.0.0

'''
Module to download a single video from youtube
'''
import threading
import logging
from pytube import YouTube
from queue import Queue,Empty
from settings import settings


class Downloader(threading.Thread):

    def __init__(self, name, redisClient,playlist_url, url_queue):
        super().__init__()
        self.name = name
        self.redisClient = redisClient
        self.playlist_url =playlist_url
        self.url_queue = url_queue

    def run(self):

        while True:
            try:
                url = self.url_queue.get(True, 5)
            except Empty as e:
                break

            yt = None

            def on_completed(url):
                '''
                callback function for stream download complete events.
                :param url:
                :return:
                '''
                # with self.lock:
                self.redisClient.hash_set(self.playlist_url, url, 'True')
                logging.info('Download successfully by %s:%s' % (threading.current_thread().name, url))
                print('Download successfully by %s::::%s' % (threading.current_thread().name, url))

            try:
                yt = YouTube(url=url, on_complete_callback=on_completed(url))
                yt.streams.first().download(settings.FILE_PATH)
            except Exception as e:
                print(e)
                print("Download failed by %s" % (threading.current_thread().name))
