from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()

class Whisper(Base):
    __tablename__ = 'whispers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    whisper_id = Column(String)
    sender_id = Column(Integer)
    reciver_id = Column(Integer)
    username = Column(String)
    message = Column(String)

class ApprovedUser(Base):
    __tablename__ = 'approved_users'
    user_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, primary_key=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def store_whisper(whisper_id, sender_id, reciver_id, username, message):
    with Session() as session:
        whisper = Whisper(whisper_id=whisper_id, sender_id=sender_id, reciver_id=reciver_id, username=username, message=message)
        session.add(whisper)
        session.commit()

def get_whisper(whisper_id):
    with Session() as session:
        return session.query(Whisper).filter_by(whisper_id=whisper_id).first()

def add_approved_user(user_id, group_id):
    with Session() as session:
        existing_user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
        if not existing_user:
            new_user = ApprovedUser(user_id=user_id, group_id=group_id)
            session.add(new_user)
            session.commit()

def remove_approved_user(user_id, group_id):
    with Session() as session:
        user_to_remove = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
        if user_to_remove:
            session.delete(user_to_remove)
            session.commit()

def is_approved_user(user_id, group_id):
    with Session() as session:
        user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
        return user is not None

def get_approved_users(group_id):
    with Session() as session:
        users = session.query(ApprovedUser).filter_by(group_id=group_id).all()
        return [(user.user_id, user.group_id) for user in users]

def init_db():
    Base.metadata.create_all(bind=engine)

init_db()
