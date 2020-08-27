from db import db
import json
class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),unique=True)
    password = db.Column(db.String(60))
    is_admin = db.Column(db.Boolean,unique=False, default=False)

    def __init__(self,username,password,is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


    def toJSON(self):
        return {'id' : self.id ,'username' : self.username,'is_admin' : self.is_admin}




    