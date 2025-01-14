import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

BASE = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SESSION = SessionLocal()

class UserScore(BASE):
    __tablename__ = "user_scores"
    user_id = Column(String(255), primary_key=True)
    username = Column(String(255))
    score = Column(Integer, default=0)

    def __init__(self, user_id, username, score=0):
        self.user_id = str(user_id)
        self.username = str(username)
        self.score = score

BASE.metadata.create_all(bind=engine)

def add_or_update_user(user_id, username):
    user = SESSION.query(UserScore).get(str(user_id))
    if not user:
        user = UserScore(user_id=str(user_id), username=str(username))
        SESSION.add(user)
    SESSION.commit()

def add_point_to_winner(user_id):
    user = SESSION.query(UserScore).get(str(user_id))
    if user:
        user.score += 1
        SESSION.commit()

def get_user_score(user_id):
    user = SESSION.query(UserScore).get(str(user_id))
    return user.score if user else 0

def store_whisper(whisper_id, sender_id, username, message):
    whisper = UserScore(user_id=whisper_id, username=username, score=0) 
    SESSION.add(whisper)
    SESSION.commit()

def get_whisper(whisper_id):
    whisper = SESSION.query(UserScore).filter(UserScore.user_id == whisper_id).first()
    return whisper
