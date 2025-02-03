from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///user_dates.db"
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

class UserDates(Base):
    __tablename__ = 'user_dates'

    user_id = Column(Integer, primary_key=True)
    saved_date = Column(String, nullable=False)

class Whisper(Base):
    __tablename__ = 'whispers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    whisper_id = Column(String, unique=True)
    sender_id = Column(Integer)
    reciver_id = Column(Integer)
    username = Column(String)
    message = Column(String)
    timestamp = Column(String)

Base.metadata.create_all(engine)

def save_date(user_id, date):
    existing_date = session.query(UserDates).filter_by(user_id=user_id).first()
    if existing_date:
        existing_date.saved_date = date
    else:
        new_date = UserDates(user_id=user_id, saved_date=date)
        session.add(new_date)
    session.commit()

def get_saved_date(user_id):
    user_date = session.query(UserDates).filter_by(user_id=user_id).first()
    return user_date.saved_date if user_date else None

def store_whisper(whisper_id, sender_id, reciver_id, username, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    whisper = Whisper(
        whisper_id=whisper_id,
        sender_id=sender_id,
        reciver_id=reciver_id,
        username=username,
        message=message,
        timestamp=timestamp
    )
    session.add(whisper)
    session.commit()

def get_whisper(whisper_id):
    return session.query(Whisper).filter_by(whisper_id=whisper_id).first()

def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
