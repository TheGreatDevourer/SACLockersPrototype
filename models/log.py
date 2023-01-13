from database import db

class Log (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    message = db.Column(db.String, nullable=False)
    timestamp =  db.Column(db.DateTime, nullable= False)


    def __init__(self, id, message,timestamp):
        self.id = id
        self.message = message
        self.timestamp =  datetime.strptime(timestamp,'%Y-%m-%dT%H:%M')
        
            
    def toJSON(self):
        return {
            'id': self.locker_code,
            'message':self.message,
            'timestamp': self.timestamp,
        }