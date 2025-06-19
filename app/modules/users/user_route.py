from typing import Optional
from fastapi import APIRouter, BackgroundTasks
from app.auth.auth_bearer import JWTBearer
from config.database import getDb
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas import user_schema
from app.modules.users.user_service import UserService
from config.database import msg
from app.schemas.response_schema import ResponseSchema
from fastapi_pagination import Params

router = APIRouter(prefix="/user",tags=['Users'])

@router.get('/list', summary="List of all users", dependencies = [Depends(JWTBearer())])
def user_list(params: Params = Depends(), search_string: Optional[str] = None, sort_by: Optional[str] = None, sort_direction: Optional[str] = None, db: Session = Depends(getDb)):
    user_list = UserService.list(params = params, search_string = search_string, sort_by = sort_by, sort_direction = sort_direction, db = db)
    if user_list is not None:
        return ResponseSchema(status=True, response=msg["user_list"],data=user_list)
    elif user_list is False:
        return ResponseSchema(status=False, response=msg["user_list_not_found"],data=None)

@router.get('/{id}', summary="Get user by ID", dependencies = [Depends(JWTBearer())])
def user_show(id:int, db: Session = Depends(getDb)):
    user_show = UserService.show(id = id,  db = db)
    if user_show is not None and type(user_show) == dict:
        return ResponseSchema(status=True, response=msg["user_found"],data=user_show)
    elif user_show is None:
        return ResponseSchema(status=False, response=msg["user_not_found"],data=None)

@router.post('/create', summary="Create new user")
def user_create(background_tasks: BackgroundTasks, request: user_schema.User, db: Session = Depends(getDb)):
    user_create = UserService.create(request = request, db = db, background_tasks = background_tasks)
    if user_create is not None and type(user_create) == dict:
        return ResponseSchema(status=True, response=msg["user_created"],data=user_create)
    elif user_create is False:
        return ResponseSchema(status=False, response=msg["user_exists"],data=None)

@router.put('/update/{id}', summary="Update user", dependencies = [Depends(JWTBearer())])
def user_update(id:int, request: user_schema.User, db: Session = Depends(getDb)):
    user_update = UserService.update(id = id, request = request, db = db)
    if user_update is not None and type(user_update) == dict:
        return ResponseSchema(status=True, response=msg["user_updated"],data=user_update)
    elif user_update is False or user_update is None:
        return ResponseSchema(status=False, response=msg["user_not_found"],data=None)

@router.delete('/{id}', summary="Delete user", dependencies = [Depends(JWTBearer())])
def user_delete(id:int, db: Session = Depends(getDb)): 
    user_delete = UserService.delete(id = id, db = db)
    if user_delete is True:
        return ResponseSchema(status=True, response=msg["user_deleted"],data=user_delete)
    elif user_delete is False:
        return ResponseSchema(status=False, response=msg["user_not_found"],data=None)