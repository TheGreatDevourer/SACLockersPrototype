from models import Locker
from database import db
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

def add_new_locker(locker_code,area,locker_type,status,key_id):
    try:
        locker = Locker(locker_code,area,locker_type,status,key_id)
        db.session.add(locker)
        db.session.commit()
        return locker
    except SQLAlchemyError:
        db.session.rollback()
        return []

def get_lockers_available():
    locker_list = Locker.query.filter_by(status = "FREE").all()
    if not locker_list:
        return []
    return [l.toJSON() for l in locker_list]

def get_locker_id(id):
    locker = Locker.query.filter_by(id = id).first()
    if not locker:
        return []
    return locker.toJSON()

def get_all_lockers():
    locker_list = Locker.query.all()
    if not locker_list:
        return []
    return [l.toJSON() for l in locker_list]

def get_lockers_unavailable():
    locker_list = Locker.query.filter_by(or_(status == "RENTED" , status == "REPAIR")).all()
    if not locker_list:
        return []
    return [l.toJSON() for l in locker_list]
    