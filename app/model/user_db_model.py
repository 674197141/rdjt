from sqlalchemy import func

from app import Base_DB_Model, db


class UserDb(Base_DB_Model):
    __tablename__ = 'table_user_test'

    user_id = db.Column(db.BigInteger, primary_key=True, info='用户id')
    user_name = db.Column(db.String(125))
    password = db.Column(db.String(64))
    phone = db.Column(db.String(11))
    birthdata = db.Column(db.DATETIME)

    @classmethod
    def create(cls,user_name,password,phone,birthdata,**kwargs):
        t = cls()
        t.user_id = func.uuid_short()
        t.user_name = user_name
        t.password = password
        t.phone = phone
        t.birthdata = birthdata
        db.session.add(t)
        db.session.commit()
        return True
