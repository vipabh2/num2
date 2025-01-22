from sqlalchemy import create_engine, Column, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

Base = declarative_base()

class ApprovedUser(Base):
    __tablename__ = 'approved_users'
    user_id = Column(BigInteger, primary_key=True)
    group_id = Column(BigInteger, primary_key=True)
    def __repr__(self):
        return f"<ApprovedUser(user_id={self.user_id}, group_id={self.group_id})>"

engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_approved_user(user_id, group_id):
    if not is_approved_user(user_id, group_id):
        approved_user = ApprovedUser(user_id=user_id, group_id=group_id)
        session.add(approved_user)
        session.commit()

def get_approved_users(group_id):
    users = session.query(ApprovedUser).filter_by(group_id=group_id).all()
    user_list = []
    for user in users:
        user_list.append((user.user_id, user.group_id))
    return user_list

def remove_approved_user(user_id, group_id):
    user_to_remove = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
    if user_to_remove:
        session.delete(user_to_remove)
        session.commit()

def is_approved_user(user_id, group_id):
    user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
    return user is not None
