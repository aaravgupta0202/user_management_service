import os
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.roles_model import Roles
from app.models.permissions_model import Permissions
from datetime import datetime, timezone
from config.database import Base

class RoleHasPermissions(Base):
    __tablename__ = 'te_role_has_permissions'

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer)
    permission_id = Column(String(200))

    permission = relationship(Permissions, backref = "te_role_has_permissions", primaryjoin = 'foreign(RoleHasPermissions.permission_id) == remote(Permissions.id)', lazy = "select")
    role = relationship(Roles, backref = "te_role_has_permissions", primaryjoin = 'foreign(RoleHasPermissions.role_id) == remote(Roles.id)', lazy = "select")