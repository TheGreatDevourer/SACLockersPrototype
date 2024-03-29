from models import Locker
from models.locker import Status, LockerTypes,Key
from database import db
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from flask import flash
from controllers.log import create_log

def add_new_locker(locker_code,locker_type,status,key):
    new_code=get_locker_id(locker_code)
    if not new_code:
        try:
            locker = Locker(locker_code,locker_type,status,key)
            db.session.add(locker)
            db.session.commit()
            return locker
        except SQLAlchemyError as e:
            create_log(locker_code,type(e),datetime.now())
            flash("Unable to Add new Area. Check Error Log for more Details")
            db.session.rollback()
            return []
    create_log(locker_code,"Locker Already Exists",datetime.now())
    flash("Unable to Add new Area. Check Error Log for more Details")
    return []

def get_lockers_available():
    locker_list = Locker.query.filter_by(status = Status.FREE).all()
    if not locker_list:
        return []
    return [l.toJSON() for l in locker_list]

def get_locker_id(id):
    locker = Locker.query.filter_by(locker_code = id).first()
    if not locker:
        return None
    return locker

def get_all_lockers():
    locker_list = Locker.query.all()
    if not locker_list:
        return []
    return [l.toJSON() for l in locker_list]

def rent_locker(id):
    locker = get_locker_id(id)
    if not locker or Locker.status == Status.RENTED:
        flash("locker already Rented")
        return None
    locker.status = Status.RENTED
    try:
        db.session.add(locker)
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to Rent Locker. Check Error Log for more Details")
        db.session.rollback()
        return None

def release_locker(id):
    locker = get_locker_id(id)
    
    if not locker :
        return None
    
    locker.status = Status.FREE
    
    try:
        db.session.add(locker)
        db.session.commit()
        
        return locker
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to rent Locker. Check Error Log for more Details")
        db.session.rollback()
        return None

def delete_locker(id):
    locker = get_locker_id(id)
    if not locker:
        return None
    try:
        db.session.delete(locker)
        db.session.commit()
        return locker
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to delete Locker. Check Error Log for more Details")
        db.session.rollback()
        return None
    
def update_key(id, new_key):
    locker = get_locker_id(id)
    if not locker:

        return None
    try:
         if new_key.upper() in Key.__members__:
            locker.key = Key[new_key.upper()]
            db.session.add(locker)
            db.session.commit()
            return locker
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to update key. Check Error Log for more Details")
        db.session.rollback()
        return None

def update_locker_status(id, new_status):
    locker = get_locker_id(id)
    if not locker:

        return None
    try:
        if new_status.upper() in Status.__members__:
            locker.status = Status[new_status.upper()]
            db.session.add(locker)
            db.session.commit()
            return locker
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to update locker status. Check Error Log for more Details")
        db.session.rollback()
        return None

def update_locker_type(id, new_type):
    locker = get_locker_id(id)
    if not locker:

        return None
    try:
        if new_type.upper() in LockerTypes.__members__:
            locker.locker_type = LockerTypes[new_type.upper()]
            db.session.add(locker)
            db.session.commit()
            return locker
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to update locker type. Check Error Log for more Details")
        db.session.rollback()
        return None


def getStatuses():
    return [ e.value for e in Status ]

def getLockerTypes():
    return [ e.value for e in LockerTypes]
    
def getKey():
    return [ e.value for e in Key]