from database import db 
from models import TransactionLog
from models.transactionLog import TransactionType
from sqlalchemy.exc import SQLAlchemyError
from flask import flash
from datetime import datetime
from controllers.log import create_log
def add_new_transaction(rent_id, currency, transaction_date, amount, description, t_type):
    try:
        new_transaction = TransactionLog(rent_id, currency,transaction_date, amount, description, t_type)
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction
    except SQLAlchemyError  as e:
        create_log(id,type(e),datetime.now())
        flash("Unable to Add new Transaction.Check Error Log for more Details")
        db.session.rollback()
        return []

def get_transaction_id(id):
    transaction = TransactionLog.query.filter_by(id = id)

    if not transaction:
        flash("Transaction does not exist")
        return []
    return transaction

def get_transaction_json(id):
    transaction = get_transaction_id(id)

    if not transaction:
        return []
    return transaction.toJSON()

def get_all_transactions():
    transactions = TransactionLog.query.all()

    if not transactions:
        return []

    return [t.toJSON() for t in transactions]

def getT_Type():
    return [ e.value for e in TransactionType ]

    