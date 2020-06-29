# coding=utf-8
# auther：Liul5
# date：9/18/2019 9:48 AM
# tools：PyCharm
# Python：3.7.3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


def session_delete(table_obj):
    db.session.delete(table_obj)
    msg = session_commit()
    return msg


def session_add(table_obj):
    db.session.add(table_obj)
    msg = session_commit()
    return msg


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
    finally:
        db.session.close()


if __name__ == "__main__":
    db.create_all()
