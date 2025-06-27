from datetime import datetime, timezone
import traceback
from fastapi import BackgroundTasks, Depends, Request
from app.hashing.hashing import hash_
from app.helper.general_helper import GeneralHelper
from app.models.password_reset import PasswordReset
from app.models.user_model import User
from app.schemas.change_password_schema import SubmitResetSchema, VerifyOTPSchema, ChangePasswordSchema
from config.database import getDb
from sqlalchemy.orm import Session, load_only


class ResetPassword :
    def submit_reset(background_tasks: BackgroundTasks, request: SubmitResetSchema, db: Session = Depends(getDb)):
        try:

            user = db.query(User).filter(User.email == request.email, User.deleted_at == None).first()
            if not user:
                return False
            else:
                otp = GeneralHelper.generate_otp()
                reset = PasswordReset(
                    email = request.email,
                    otp = otp,
                    is_verified = 0)
                db.add(reset)
                db.commit()
                background_tasks.add_task(GeneralHelper.send_otp, user.name, user.surname, request.email, otp, background_tasks)
                return True
        
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)

            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
        
    def verify_otp(request: VerifyOTPSchema, db: Session = Depends(getDb)):
        try:

            user = db.query(PasswordReset).filter(PasswordReset.email == request.email, PasswordReset.is_verified == 0).order_by(PasswordReset.id.desc()).first()
            if not user:
                return 2
            elif (request.otp == user.otp) and (request.email == user.email):
                user.is_verified = 1
                user.updated_at = datetime.now(timezone.utc)
                db.commit()
                db.refresh(user)
                return 1
            else:
                return 3
        
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)

            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
        
    def change_password(request: ChangePasswordSchema, db: Session = Depends(getDb)):
        try:
            
            user = db.query(User).filter(User.email == request.email, User.deleted_at == None).first()
            if not user:
                return 2
            else:
                user.password = hash_(request.password)
                db.commit()
                return 1
            
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)

            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)