from fastapi import APIRouter
from config.database import getDb
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.login_schema import UserLogin
from app.modules.login.login_service import LoginService
from config.database import msg
from app.schemas.response_schema import ResponseSchema

router = APIRouter(prefix="/login",tags=['Login'])

@router.post('/', summary="Login into account")
def user_login(request: UserLogin, db: Session = Depends(getDb)):
    user_login = LoginService.login(request = request, db = db)
    if user_login is not None and type(user_login) == dict:
        return ResponseSchema(status=True, response=msg["user_login"],data=user_login)
    elif user_login is False:
        return ResponseSchema(status=False, response=msg["wrong_pass"],data=None)
    elif user_login is None:
        return ResponseSchema(status=False, response=msg["something_went_wrong"],data=None)