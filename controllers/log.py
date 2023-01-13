from models import Log

from datetime import datetime
from database import db 
from sqlalchemy.exc import SQLAlchemyError

def create_log(id, message,timestamp):
    try:
        log = Log(id, message,timestamp)
        db.session.add(log)
        db.session.commit(log)
        return log
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()   
        return None

def get_all_logs():
    logs = Log.query.all()

    if not logs:
        return None

    return[l.toJSON() for l in logs]