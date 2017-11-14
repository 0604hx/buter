"""
add on 2017-11-14 15:42:54
"""
from datetime import datetime

from app.server import db


class Application(db.Model):
    __tablename__ = "app"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    remark = db.Column(db.TEXT, unique=False)
    addDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Application #{} name={} remark={} addOn={}>'.format(self.id, self.name,self.remark,self.addDate)