from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime 
DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()

class Whisper(Base):
    __tablename__ = 'whispers'

    id = Column(Integer, primary_key=True, autoincrement=False)
    whisper_id = Column(String, unique=True)
    sender_id = Column(Integer)
    reciver_id = Column(Integer)
    username = Column(String)
    message = Column(String)
    timestamp = Column(String) 
def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

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
