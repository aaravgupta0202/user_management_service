from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from config.database import Base

class PasswordReset(Base):
    __tablename__ = 'te_password_reset'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100))
    otp = Column(String(6))
    is_verified = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=None)