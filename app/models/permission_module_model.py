from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from config.database import Base

class User(Base):
    __tablename__ = 'te_roles'

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String(150))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))