# -*- coding=utf-8 -*-
import grequests
import re
import os
import sys
from time import clock
from . import celery,db
from .models import Context

extractpicre = re.compile(r'(?<=<photo-url max-width="1280">).+?(?=</photo-url>)',flags=re.S)   #search for url of maxium size of a picture, which starts with '<photo-url max-width="1280">' and ends with '</photo-url>'
extractvideore=re.compile('''poster='(.*?)'[\w\W]*?/tumblr_(.*?)" type="video/mp4"''')


video_links = []
pic_links = []
vhead = 'https://vt.tumblr.com/tumblr_%s.mp4'
api_url='http://%s.tumblr.com/api/read?&num=50&start='
query_urls=[]


def getpost(uid,query_urls):
    url='http://%s.tumblr.com/api/read?&num=50'%uid
    page=grequests.map([grequests.get(url)])[0].content
    total=re.findall('<posts start="0" total="(.*?)">',page)[0]
    total=int(total)
    a=[i*50 for i in range(total/50)]
    ul=api_url%uid
    for i in a:
        query_url=ul+str(i)
        query_urls.append(query_url)

def run(query_urls):
    rs=[grequests.get(url) for url in query_urls]
    responses=grequests.map(rs,size=10)
    for resp in responses:
        content = resp.content
        videos = extractvideore.findall(content)
        video_links.extend([(v[0],vhead % v[1]) for v in videos])
        pic_links.extend(extractpicre.findall(content))

def write(name):
    videos=[(i[0],i[1].replace('/480','')) for i in video_links]
    pictures=pic_links
    for url in list(set(videos)):
        poster,video=url
        data=Context.query.filter_by(id=name,urls=video).first()
        if not data:
            data=Context(name,video,1,poster)
            db.session.add(data)
        else:
            data=Context.query.filter_by(id=name,urls=video).first()
            data.poster=poster
            db.session.add(data)
    for url in list(set(pictures)):
        dat=Context.query.filter_by(id=name,urls=url).first()
        if not dat:
            data=Context(name,url,0,url)
            db.session.add(data)
        else:
            data=Context.query.filter_by(id=name,urls=url).first()
            data.poster=url
            data.urls=url
            db.session.add(data)
    db.session.commit()


@celery.task
def TumblrGet(name):
    now=clock()
    getpost(name,query_urls)
    run(query_urls)
    write(name)
    print u"%s解析完毕，请查看同目录下的文件。花费时间：%.1f"%(name,clock()-now)
    print u"图片%d张，视频%d部"%(len(pic_links),len(video_links))
