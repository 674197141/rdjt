from app import Base_DB_Model, db


class UserDb(Base_DB_Model):
    __tablename__ = 'user'

    user_id = db.Column(db.BigInteger, primary_key=True, info='用户id')
    user_name = db.Column(db.String(125))
    password = db.Column(db.String(64))
    phone = db.Column(db.String(11))
    birthdata = db.Column(db.DATETIME)
