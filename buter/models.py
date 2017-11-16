"""
add on 2017-11-14 15:42:54
"""
from datetime import datetime

from .server import db


class IdMixin(object):
    id = db.Column(db.Integer, primary_key=True)


class Application(IdMixin, db.Model):
    __tablename__ = "app"

    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    version = db.Column(db.String(10), nullable=False)
    remark = db.Column(db.TEXT, unique=False)
    addDate = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # def __init__(self, name, id=0, remark=None, version=None):
    #     self.name = name
    #     self.remark = remark
    #     self.version = version
    #     if id and id > 0:
    #         self.id = id

    def __repr__(self):
        return '<Application #{} name={} version={} remark={} addOn={}>'.format(
            self.id,
            self.name,
            self.version,
            self.remark,
            self.addDate
        )

    __str__ = __repr__