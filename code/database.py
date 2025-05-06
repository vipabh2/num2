from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
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
session = Session()

def store_whisper(whisper_id, sender_id, reciver_id, username, message):
    whisper = Whisper(whisper_id=whisper_id, sender_id=sender_id, reciver_id=reciver_id, username=username, message=message)
    session.add(whisper)
    session.commit()

def get_whisper(whisper_id):
    return session.query(Whisper).filter_by(whisper_id=whisper_id).first()

def init_db():
    Base.metadata.create_all(bind=engine)

init_db()
