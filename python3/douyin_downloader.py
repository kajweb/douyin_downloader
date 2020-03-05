#!/usr/bin/pytho3
# -*- coding: UTF-8 -*- 

##################################################################
##													      		##
## 		  To Download DOUYIN Video Without Watermark		    ##
## 		  	  测试URL：https://v.douyin.com/gWc3BC	     		##
## 		GITHUB：https://github.com/kajweb/douyin_downloader		##
##															    ##
##################################################################

import requests
import configparser
import os
from bs4 import BeautifulSoup

# 屏蔽SSL错误（提醒）
from requests.packages import urllib3
urllib3.disable_warnings()

def getHeaders( filename, key ):
	conf = configparser.ConfigParser()
	conf.read( filename );
	confDict = dict(conf._sections);
	headers = dict(confDict[key]);
	return headers;

def getAndroidHeaders( filename, key ):
	conf = configparser.ConfigParser()
	conf.read( filename );
	confDict = dict(conf._sections);
	headers = dict(confDict[key]);
	return headers;

def parse_douyin( url, headers ):
	# 获得视频的源地址
	res = requests.get( url, headers=headers, verify=False );
	# todo 判断是否get成功
	res.encoding = 'utf-8'
	data = res.text
	pageObj = BeautifulSoup(data, 'lxml');
	videoObj = pageObj.find("video",class_='video-player');
	playAddr = videoObj.get("src");
	# 替换为下载的url
	videoAddr = playAddr.replace("/playwm/","/play/");
	videoId = data.split("itemId: \"")[1].split("\",")[0]
	return {
		"playAddr": playAddr,
		"addr": videoAddr,
		"id": videoId
	}

def mkdir( folder ):
    isExists = os.path.exists(folder)
    if not isExists:
        os.makedirs( folder, 0o777 );
        return True;
    return False;

def download_douyin( parseDouyin, headers ):
	# 懒得创建文件夹，直接跟文件同一个目录算了 todo
	folder = "download/";
	mkdir(folder);
	videoBin = requests.get( parseDouyin['addr'], headers=headers, verify=False );
	_filename = folder + parseDouyin['id'] + ".mp4";
	fullName = os.path.abspath( _filename );
	with open( fullName, "wb" )as f:
	        f.write(videoBin.content)
	        f.close()
	return fullName;


if __name__ == '__main__':
	headers = getHeaders( "config.ini", "headers" );
	androidHeaders = getHeaders( "config.ini", "android-headers" );
	while True:
		url = input("请输入需要下载的视频url：");
		# todo 判断url有效性
		parseData = parse_douyin( url, androidHeaders);
		print( "解析出的视频源地址为：" + parseData['addr'] );
		# 下载视频
		fullName = download_douyin( parseData, androidHeaders );
		print( "下载完成，", "下载视频Id为：",parseData['id'], "\n" );
		print( "请求播放视频中……\n" );
		playFlag = os.system( fullName )
		print( fullName )
		if playFlag==0:
			print( "播放视频成功\n" );
		else:
			print( "播放视频失败\n" );
