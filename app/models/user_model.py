from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from config.database import Base

class User(Base):
    __tablename__ = 'te_users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(500))
    surname = Column(String(500))
    email = Column(String(100))
    password = Column(String(150))
    profile_image = Column(String(500), default=None)
    mobile_no = Column(String(15))
    city = Column(String(200))
    state = Column(String(100))
    country = Column(String(100))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=None)
    deleted_at = Column(DateTime, default=None)