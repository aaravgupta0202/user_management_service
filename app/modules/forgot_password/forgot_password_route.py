from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.modules.forgot_password.forgot_password_service import ResetPassword
from config.database import msg
from app.auth.auth_bearer import JWTBearer
from app.schemas.response_schema import ResponseSchema
from config.database import getDb
from app.schemas.change_password_schema import SubmitResetSchema, VerifyOTPSchema, ChangePasswordSchema


router = APIRouter(prefix="",tags=['Reset Password'])

@router.post('/reset_password', summary="Apply for resetting password")
def submit_reset(background_tasks: BackgroundTasks, request: SubmitResetSchema, db: Session = Depends(getDb)):
    submit_reset = ResetPassword.submit_reset(background_tasks = background_tasks, request = request, db = db)
    if submit_reset is not None:
        return ResponseSchema(status=True, response=msg["otp_sent"],data=None)
    elif submit_reset is None:
        return ResponseSchema(status=False, response=msg["user_not_found"],data=None)
    
@router.post('/verify_otp', summary="Verify your OTP")
def verify_otp(request: VerifyOTPSchema, db: Session = Depends(getDb)):
    verify_otp = ResetPassword.verify_otp(request = request, db = db)
    if verify_otp == 1:
        return ResponseSchema(status=True, response=msg["otp_verified"],data=None)
    elif verify_otp == 3:
        return ResponseSchema(status=False, response=msg["otp_wrong"],data=None)
    elif verify_otp == 2:
        return ResponseSchema(status=False, response=msg["email_wrong"],data=None)
    
@router.post('/new_password', summary="Set a new password")
def new_password(request: ChangePasswordSchema, db: Session = Depends(getDb)):
    new_password = ResetPassword.change_password(request = request, db = db)
    if new_password == 1:
        return ResponseSchema(status=True, response=msg["password_changed"],data=None)
    elif new_password == 2:
        return ResponseSchema(status=False, response=msg["email_wrong"],data=None)