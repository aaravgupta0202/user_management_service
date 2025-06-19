from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from config.database import Base

class Permissions(Base):
    __tablename__ = 'te_permissions'

    id = Column(Integer, primary_key=True, index=True)
    permission_module = Column(Integer)
    permission_name = Column(String(200))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))