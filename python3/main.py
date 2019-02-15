# python3 code
# to download douyin video without watermark
# 测试URL：http://v.douyin.com/FLBYQq

import requests
import configparser

def getHeaders( filename, key ):
	conf = configparser.ConfigParser()
	conf.read( filename );
	confDict = dict(conf._sections);
	headers = dict(confDict[key]);
	return headers;

def parse_douyin( url, headers ):
	# 获得视频的源地址
	res = requests.get(url,headers=headers);
	# todo 判断是否get成功
	res.encoding = 'utf-8'
	data = res.text
	cover = data.split("cover: \"")[1].split("\"")[0]
	playAddr = data.split("playAddr: \"")[1].split("\",")[0]
	videoId = playAddr.split("video_id=")[1].split("&")[0]
	# 替换为下载的url
	videoAddr = playAddr.replace("/playwm/","/play/");
	return {
		"cover": cover,
		"playAddr": playAddr,
		"addr": videoAddr,
		"id": videoId
	}

def download_douyin( parseDouyin, headers ):
	# 懒得创建文件夹，直接跟文件同一个目录算了 todo
	videoBin = requests.get( parseDouyin['addr'], headers=headers );
	filename = parseDouyin['id'] + ".mp4";
	with open( filename, "wb") as f:
	        f.write(videoBin.content)
	        f.close()

headers = getHeaders( "config.ini", "headers" );
while True:
	url = input("请输入需要下载的视频url：");
	# todo 判断url有效性
	parseData = parse_douyin( url, headers);
	print( "解析出的视频源地址为：" + parseData['addr'] );
	# 下载视频
	download_douyin( parseData, headers );
	print( "下载完成，", "下载视频Id为：",parseData['id'], "\n" );