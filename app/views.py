#-*- coding=utf-8 -*-
from app import app, db
from app.models import *
from flask import render_template, redirect, request, url_for, flash, session, jsonify, make_response
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import subprocess
import os
from datetime import datetime
#from .tumblr_task import TumblrGet
import re
import requests
import os

basedir = os.path.abspath('.')
clawer = os.path.join(basedir, 'tumblr.py')

#VIDEOREGEX = re.compile('http://media.tumblr.com/(.*?)_frame1')
VIDEOREGEX = re.compile(
    '<meta property="og:image".*?media.tumblr.com/tumblr_(.*?)_')
POSTERREGEX = re.compile('<meta property="og:image" content="(.*?)"')
IMAGEREGEX = re.compile(
    '<meta property="og:image" content="(.*?)" /><meta property="og:image:height"')
vhead = 'https://vt.tumblr.com/tumblr_%s.mp4'

HOME = 'http://%s.tumblr.com/api/read?&num=50'


def check(uid):
    url = HOME % uid
    try:
        cont = requests.get(url)
        if cont.ok:
            if int(re.findall('<posts start="0" total="(.*?)">', cont.content)[0]) != 0:
                return True
            else:
                return False
        else:
            return False
    except:
        return False


@app.context_processor
def form_trans():
    return dict(method='method')


@app.route('/')
def index():
    id = ID.query.order_by(ID.updateTime.desc()).limit(5).all()
    return render_template('index.html', ids=id)


@app.route('/get', methods=['POST', 'GET'])
def getTumblr():
    if request.method == 'POST':
        id = request.form.get('id')
        if 'tumblr.com/post' in id:
            try:
                video = ''
                cont = requests.get(id).content
                pictures = IMAGEREGEX.findall(cont)
                vid = VIDEOREGEX.findall(cont)
                poster = POSTERREGEX.findall(cont)
                isvideo = 0
                if vid:
                    video = vhead % vid[0]
                    poster = poster[0]
                    isvideo = 1
                if len(vid) + len(pictures) <> 0:
                    flash('解析成功')
                    return render_template('show_single.html', video=video, pictures=pictures, poster=poster, isvideo=isvideo)
                else:
                    flash('解析失败')
                    return redirect(url_for('index'))
            except Exception, e:
                print e
                flash('解析失败')
                return redirect(url_for('index'))
        else:
            if check(id):
                is_exists = ID.query.filter_by(id=id).first()
                if is_exists is None:
                    now = datetime.now()
                    inserttime = now.strftime('%Y%m%d %H:%M:%S')
                    a = ID(id=id, updateTime=inserttime, parseTimes=1)
                    db.session.add(a)
                    db.session.commit()
                else:
                    now = datetime.now()
                    is_exists.updateTime = now.strftime('%Y%m%d %H:%M:%S')
                    is_exists.parseTimes += 1
                    db.session.add(is_exists)
                    db.session.commit()
                subprocess.Popen('python {clawer} {id}'.format(
                    clawer=clawer, id=id), shell=True)
                return redirect(url_for('showid', id=id))
            else:
                flash('解析失败')
                return redirect(url_for('index'))
    return 'hello world'


@app.route('/show/<id>')
def showid(id):
    videos = Context.query.filter_by(id=id, isvideo=1).limit(10).all()
    pictures = Context.query.filter_by(id=id, isvideo=0).limit(10).all()
    if len(videos) + len(pictures) == 0:
        isparse = 0
    else:
        isparse = 1
    return render_template('show.html', id=id, videos=videos, pictures=pictures, isparse=isparse)


@app.route('/showmore')
def showmore():
    id = request.args.get('id')
    type = request.args.get('type')
    page = request.args.get('page', 1, type=int)
    if type == 'video':
        pagination = Context.query.filter_by(id=id, isvideo=1).paginate(
            page, per_page=20, error_out=False)
    else:
        pagination = Context.query.filter_by(id=id, isvideo=0).paginate(
            page, per_page=20, error_out=False)
    items = pagination.items
    return render_template('showmore.html', id=id, pagination=pagination, type=type, items=items)


@app.route('/download')
def download():
    id = request.args.get('id')
    type = request.args.get('type')
    if type == 'video':
        isvideo = 1
    else:
        isvideo = 0
    query_result = Context.query.filter_by(id=id, isvideo=isvideo).all()
    if len(query_result) <> 0:
        content = ''
        for line in query_result:
            content += '%s\n' % line.urls
        response = make_response(content)
        response.headers["Content-Disposition"] = "attachment; filename=%s.txt" % (
            id + "_" + type)
        return response
    else:
        return redirect(url_for('index'))
