from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from config.database import Base

class UserHasRoles(Base):
    __tablename__ = 'te_user_has_roles'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    role_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))