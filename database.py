from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ApprovedUser(Base):
    __tablename__ = 'approved_users'
    
    user_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, primary_key=True)

engine = create_engine('sqlite:///approved_users.db', echo=True)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_approved_user(user_id, group_id):
    existing_user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
    if not existing_user:
        new_user = ApprovedUser(user_id=user_id, group_id=group_id)
        session.add(new_user)
        session.commit()

def remove_approved_user(user_id, group_id):
    user_to_remove = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
    if user_to_remove:
        session.delete(user_to_remove)
        session.commit()

def is_approved_user(user_id, group_id):
    user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
    return user is not None
    
def get_approved_users(group_id):
    users = session.query(ApprovedUser).filter_by(group_id=group_id).all()
    user_list = []
    for user in users:
        user_list.append((user.user_id, user.group_id))
    return user_list
def init_db():
    Base.metadata.create_all(bind=engine)

init_db()
