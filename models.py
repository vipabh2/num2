from sqlalchemy import Column, Integer, String
from db import BASE, SESSION, engine

class UserScore(BASE):
    __tablename__ = "user_scores"
    user_id = Column(String(255), primary_key=True) 
    username = Column(String(255))  
    score = Column(Integer, default=0)  

    def __init__(self, user_id, username, score=0):
        self.user_id = str(user_id)
        self.username = str(username)
        self.score = score

UserScore.__table__.create(bind=engine, checkfirst=True)

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
