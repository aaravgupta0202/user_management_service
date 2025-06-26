import os
import traceback
from fastapi import Depends
from app.hashing.hashing import verify_password
from app.schemas.login_schema import UserLogin
from app.models.user_model import User
from app.models.user_has_roles_model import UserHasRoles
from app.models.roles_model import Roles
from app.models.permissions_model import Permissions
from app.models.role_has_permissions_model import RoleHasPermissions
from config.database import engine
from config.database import getDb
from sqlalchemy.orm import Session, load_only
from sqlalchemy import func
from app.auth.auth_handler import create_access_token

class LoginService:
    def login(request: UserLogin, db: Session = Depends(getDb)):
            try:
                check_user = db.query(User).filter(User.email == request.email, User.deleted_at == None).first()
                if not check_user:
                    return None
                if not verify_password(request.password, check_user.password):
                    return False
                else:
                    del check_user.password
                    token = create_access_token(user_id = check_user.id,email=check_user.email)
                    check_user.__dict__["access_token"] = token["access_token"]

                    if check_user.profile_image is not None and os.getenv('BASE_URL') not in check_user.profile_image:
                        check_user.profile_image = os.path.join(os.getenv('BASE_URL'), check_user.profile_image) if check_user.profile_image else None

                    roles_list = db.query(UserHasRoles).filter(UserHasRoles.user_id == check_user.id).all()
                    role_ids_list = []
                    for i in roles_list:
                        role_ids_list.append(i.role_id)

                    roles = db.query(Roles).options(load_only(Roles.role)).filter(Roles.id.in_(role_ids_list)).all()
                    roles_list = []
                    roles_names = []
                    for i in roles:
                        roles_list.append(i.id)
                        roles_names.append(i.role)
                        
                    permissions = db.query(RoleHasPermissions).with_entities(func.group_concat(func.distinct(Permissions.id))).join(RoleHasPermissions.permission).filter(RoleHasPermissions.role_id.in_(roles_list)).scalar()

                    unique_permissions = permissions.split(",") if permissions is not None else None

                    permission_names = db.query(Permissions.permission_name).filter(Permissions.id.in_(unique_permissions)).all()

                    all_permissions = []
                    for permission_name in permission_names:
                        all_permissions.append(permission_name[0])

                    check_user.__dict__["role"] = roles
                    check_user.__dict__["permissions"] = all_permissions

                    return check_user.__dict__
            
            except Exception as e:
                traceback_str = traceback.format_exc()
                print(traceback_str)

                line_no = traceback.extract_tb(e.__traceback__)[-1][1]
                print(f"Exception occurred on line {line_no}")
                return str(e)