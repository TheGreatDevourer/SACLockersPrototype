from models import RentTypes,Rent
from database import db
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from datetime import datetime
from controllers.log import create_log

def new_rentType(period, type, price):
    try:
        rentType = RentTypes(period,type,price)
        db.session.add(rentType)
        db.session.commit()
        return rentType
    except SQLAlchemyError as e:
        create_log(type,type(e),datetime.now())
        flash("Unable to create new Rent Type. Check Error Log for more Details")
        db.session.rollback()
        return None

def get_rentType_by_id(id):
    rentType = RentTypes.query.filter_by(id = id).first()

    if not rentType:
        flash("Rent Type does not exist")
        return None

    return rentType



def get_rentType_period(period):
    rentType = RentTypes.query.filter_by(period = period)

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def get_rentType_price(price):
    rentType = RentTypes.query.filter_by(price = price)

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]

def update_rentType_price(id,new_price):
    #first check to see if a rentType exist in rent
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        return []
    try:
        rentType = get_rentType_by_id(id)

        if not rentType:
            return None
        rentType.price = new_price
        db.session.add(rentType)
        db.session.commit()
    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to update Rent Type. Check Error Log for more Details")
        db.session.rollback()
        return None

def update_rentType_period(id, period):
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        flash("Unable to update Rent Type Period. No rental Types")
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:

        return []
    
    rent_type.period = period
    try:
        db.session.add(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to update Rent Type Period. Check Error Log for more Details")
        db.session.rollback()
        return []

def update_rentType_type(id,type):
    rent = Rent.query.filter_by(rent_type = id).first()

    if rent:
        flash("Unable to update Rent Type. No rental Types")
        return []

    rent_type = get_rentType_by_id(id)

    if not rent_type:

        return []
    
    rent_type.type = type
    try:
        db.session.add(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to update Rent Type Type. Check Error Log for more Details")
        db.session.rollback()
        return []
        
def delete_rent_type(id):
    rent = Rent.query.filter_by(rent_type = id).first()
    
    if rent:
        flash("Unable to delete Rent Type. No rental Types")
        return None

    rent_type = get_rentType_by_id(id)

    if not rent_type:

        return None
    try:
        db.session.delete(rent_type)
        db.session.commit()
        return rent_type

    except SQLAlchemyError as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to delete Rent Type. Check Error Log for more Details")
        db.session.rollback()
        return []    

def get_All_rentType():
    rentType = RentTypes.query.all()

    if not rentType:
        return None
        
    return [r.toJSON() for r in rentType]