from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

engine = create_engine(DATABASE_URL, echo=False)
BASE = declarative_base()
SessionLocal = sessionmaker(bind=engine)
SESSION = SessionLocal()
if not DATABASE_URL:
    print("(رابط قاعده البيانات غير موجود"
