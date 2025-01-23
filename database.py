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

# إعداد الاتصال بقاعدة البيانات
engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(bind=engine)

# تهيئة الجلسة
Session = sessionmaker(bind=engine)

def add_approved_user(user_id, group_id):
    try:
        session = Session()  # فتح جلسة جديدة
        if not is_approved_user(user_id, group_id):
            approved_user = ApprovedUser(user_id=user_id, group_id=group_id)
            session.add(approved_user)
            session.commit()
        session.close()  # إغلاق الجلسة
    except Exception as e:
        print(f"حدث خطأ أثناء إضافة المستخدم: {e}")

def get_approved_users(group_id):
    try:
        session = Session()  # فتح جلسة جديدة
        users = session.query(ApprovedUser).filter_by(group_id=group_id).all()
        user_list = [(user.user_id, user.group_id) for user in users]
        session.close()  # إغلاق الجلسة
        return user_list
    except Exception as e:
        print(f"حدث خطأ أثناء جلب المستخدمين: {e}")
        return []

def remove_approved_user(user_id, group_id):
    try:
        session = Session()  # فتح جلسة جديدة
        user_to_remove = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
        if user_to_remove:
            session.delete(user_to_remove)
            session.commit()
        session.close()  # إغلاق الجلسة
    except Exception as e:
        print(f"حدث خطأ أثناء إزالة المستخدم: {e}")

def is_approved_user(user_id, group_id):
    try:
        session = Session()  # فتح جلسة جديدة
        user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
        session.close()  # إغلاق الجلسة
        return user is not None
    except Exception as e:
        print(f"حدث خطأ أثناء التحقق من المستخدم: {e}")
        return False
