from models import Area
from database import db
from flask import flash
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from controllers.log import create_log

def add_new_area(locker_id, description, longitude, latitude):
    try:
        new_area = Area(locker_id,description,longitude, latitude)
        db.session.add(new_area)
        db.session.commit()
        return new_area
    except SQLAlchemyError as e:
        create_log(locker_id,type(e),datetime.now())
        flash("Unable to add new Area. Check Error Log for more Details")
        db.session.rollback()
        return None

def get_area_by_id(id):
    area = Area.query.filter_by(id = id).first()
    if not area: 
        flash("Area does not exist")
        return None
    return area

def get_area_by_locker(locker_id):
    area = Area.query.filter_by(locker_id = locker_id).first()
    if not area: 
        flash("Area does not exist")
        return None
    return area

def set_description(id,new_description):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        area.description = new_description
        db.session.add(area)
        db.session.commit()
        return area
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to set description. Check Error Log for more Details")
        db.session.rollback()
        return None

def set_latitude(id, new_latitude):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        area.latitude = new_latitude
        db.session.add(area)
        db.session.commit()
        return area
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to set latitude. Check Error Log for more Details")
        db.session.rollback()
        return None

def set_longitude(id,new_longitude):
    area = get_area_by_id(id)
    
    if not area: 
        return None
    try:
        area.longitude = new_longitude
        db.session.add(area)
        db.session.commit()
        return area
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to set longitude. Check Error Log for more Details")
        db.session.rollback()
        return None

def delete_area(id):
    area = get_area_by_id(id)
    if not area: 
        return None
    try:
        db.session.delete(area)
        db.session.commit()
        return area
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to delete Area. Check Error Log for more Details")
        db.session.rollback()
        return None

def get_area_all():
    areas = Area.query.all()
    if not areas:
        return []
    return [a.toJSON() for a in areas]

