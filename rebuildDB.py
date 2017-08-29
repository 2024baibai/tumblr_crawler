#-*- coding=utf-8 -*-
from app import db

try:
    db.drop_all()
    db.create_all()
except Exception, e:
    print e
