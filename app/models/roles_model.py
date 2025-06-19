from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from config.database import Base

class Roles(Base):
    __tablename__ = 'te_roles'

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(500))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=None)
    deleted_at = Column(DateTime, default=None)
