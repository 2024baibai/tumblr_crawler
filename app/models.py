#-*- coding=utf-8 -*-
from app import db

#Tumblr
class ID(db.Model):
    __tablename__='id_table'
    id=db.Column(db.String(64),primary_key=True)
    parseTimes=db.Column(db.Integer,default=0) #解析次数
    updateTime=db.Column(db.String(64)) #最近更新时间

    def __init__(self,**kwargs):
        super(ID,self).__init__(**kwargs)

    def __repr__(self):
        return self.id

#
class Context(db.Model):
    __tablename__='context_table'
    id=db.Column(db.String(64),primary_key=True)
    urls=db.Column(db.String(200),primary_key=True)
    isvideo=db.Column(db.Integer,default=0) #0=no,1=yes
    poster=db.Column(db.String(200))

    def __init__(self,id,urls,isvideo,poster):
        self.id=id
        self.urls=urls
        self.isvideo=isvideo
        self.poster=poster

    def __repr__(self):
        return self.id
