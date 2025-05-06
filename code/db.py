from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///user_dates.db"
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()
Session = sessionmaker(bind=engine)

class UserDates(Base):
    __tablename__ = 'user_dates'

    user_id = Column(Integer, primary_key=True)
    saved_date = Column(String, nullable=False)

Base.metadata.create_all(engine)

def save_date(user_id, date):
    session = Session()
    try:
        existing_date = session.query(UserDates).filter_by(user_id=user_id).first()
        if existing_date:
            existing_date.saved_date = date
        else:
            new_date = UserDates(user_id=user_id, saved_date=date)
            session.add(new_date)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error saving date: {e}")
    finally:
        session.close()

def get_saved_date(user_id):
    session = Session()
    try:
        saved_date = session.query(UserDates).filter_by(user_id=user_id).first()
        return saved_date.saved_date if saved_date else None
    except Exception as e:
        print(f"Error retrieving date: {e}")
        return None
    finally:
        session.close()
