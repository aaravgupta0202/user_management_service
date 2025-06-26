from operator import or_
import os
import shutil
import traceback
from typing import Optional
from fastapi import BackgroundTasks, Depends, File, Form, UploadFile, Request
from fastapi.security import HTTPBearer
from app.schemas.user_schema import UserSchema
from app.models.user_model import User
from config.database import engine
from config.database import getDb
from sqlalchemy.orm import Session, load_only
from datetime import datetime, timezone
from app.hashing.hashing import hash_
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Params

from app.helper.general_helper import GeneralHelper
from datetime import datetime
from app.models.user_has_roles_model import UserHasRoles
import pandas as pd

class UserService :
    def list(params: Params = Depends(), search_string: Optional[str] = None, sort_by: Optional[str] = None, sort_direction: Optional[str] = None, db: Session = Depends(getDb)):
        try:
            user = db.query(User).filter(User.deleted_at == None).options(load_only(User.id, User.name, User.surname, User. email, User. mobile_no, User.city, User.state, User.country))
        
            if sort_direction == "desc":
                user = user.order_by(User.__dict__[sort_by].desc())
            elif sort_direction == "asc":
                user = user.order_by(User.__dict__[sort_by].asc())
            else:
                user = user.order_by(User.id.asc())
        
            if search_string:
                user = user.filter(or_(
                    User.name.like('%'+search_string+'%'),
                    User.surname.like('%'+search_string+'%'),
                ))
        
            user = paginate(user, params)
            return user
        
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)

            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def show(id: int, db: Session = Depends(getDb)):
        try:
            user = db.query(User).options(load_only(User.name, User.surname, User.email, User.mobile_no, User.city, User.state, User.country, User.profile_image)).filter(User.id == id, User.deleted_at == None).first()
            
            if user:
                if user.profile_image is not None and os.getenv('BASE_URL') not in user.profile_image:
                    user.profile_image = os.path.join(os.getenv('BASE_URL'), user.profile_image) if user.profile_image else None
                return user.__dict__
            
            return None
        
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)

            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def create(background_tasks: BackgroundTasks, request: UserSchema, db: Session = Depends(getDb)):
        try:
            check_user = db.query(User).filter(User.email == request.email, User.deleted_at == None).first()

            if check_user is not None:
                return False    
            img = GeneralHelper.UploadImageBase64(request.profile_image)

            user = User(
                name = request.name,
                surname = request.surname,
                email = request.email,
                password = hash_(request.password),
                profile_image = img,
                mobile_no = request.mobile_no,
                city = request.city,
                state = request.state,
                country = request.country)

            db.add(user)
            db.commit()
            db.refresh(user)
            
            user_has_role = UserHasRoles(
                user_id = user.id,
                role_id = 2  # Default to role_id 1 if not provided
            )

            db.add(user_has_role)
            db.commit()
            db.refresh(user_has_role)

            background_tasks.add_task(GeneralHelper.send_email, request.name, request.surname, request.email, background_tasks)
        
            db.refresh(user)

            del user.password
            user.profile_image = os.path.join(os.getenv('BASE_URL'), user.profile_image)
            return user.__dict__
        
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
 
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
        
    def create_formdata(background_tasks: BackgroundTasks, picture: UploadFile = File(None), name: str = Form(), surname: str = Form(), email: str = Form(), password: str = Form(), mobile_no: str = Form(), city: str = Form(), state: str = Form(), country: str = Form(), db: Session = Depends(getDb)):
        try:
            check_user = db.query(User).filter(User.email == email, User.deleted_at == None).first()
            picture_path = None

            if check_user is not None:
                return False
            if picture is not None:   
                picture_path = GeneralHelper.UploadImage(picture)
            else:
                picture_path = "uploads\default.jpg"
            
     
            user = User(
                name = name,
                surname = surname,
                email = email,
                password = hash_(password),
                profile_image = picture_path,
                mobile_no = mobile_no,
                city = city,
                state = state,
                country = country)

            db.add(user)
            db.commit()
            db.refresh(user)
            
            user_has_role = UserHasRoles(
                user_id = user.id,
                role_id = 2  # Default to role_id 1 if not provided
            )

            db.add(user_has_role)
            db.commit()
            db.refresh(user_has_role)

            # GeneralHelper.send_email("nirbhay.verve@gmail.com", "xdjexcbtyvgkfdlu", request.email, "ACCOUNT MADE!", f"Congratulations {request.name} {request.surname}! You account has been made!", smtp_server='smtp.gmail.com', smtp_port=465)
            background_tasks.add_task(GeneralHelper.send_email, name, surname, email, background_tasks)
        
            db.refresh(user)

            del user.password
            user.profile_image = os.path.join(os.getenv('BASE_URL'), user.profile_image)
            return user.__dict__
        
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
 
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def update(id: int, request: UserSchema, db: Session = Depends(getDb)):
        try:
            user = db.query(User).filter(User.id == id, User.deleted_at == None).first()
            img = None
            if not user:
                return False
            else:
                if request.profile_image is not None and request.is_picture_remove == 0:
                        old_path = os.path.join(os.getcwd(), user.profile_image)
                        if os.path.exists(old_path):
                            os.remove(old_path)

                        # Upload new image
                        img = GeneralHelper.UploadImageBase64(request.profile_image)
                        print(f"Image uploaded: {img}")
               
                user.name = request.name if request.name is not None else user.name
                user.surname = request.surname if request.surname is not None else user.surname
                user.password = hash_(request.password) if request.password is not None else user.password
                user.profile_image = img if img is not None else "uploads\default.jpg"
                user.mobile_no = request.mobile_no if request.mobile_no is not None else user.mobile_no
                user.email = request.email if request.email is not None else user.email
                user.city = request.city if request.city is not None else user.city
                user.state = request.state if request.state is not None else user.state
                user.country = request.country if request.country is not None else user.country
                user.updated_at = datetime.now(timezone.utc)

                db.commit()
                db.refresh(user)

                user.__dict__.pop("password")
                user.profile_image = os.path.join(os.getenv('BASE_URL'), user.profile_image)
                return user.__dict__
            
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
 
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)

    def download_excel(db: Session = Depends(getDb)):
        try:
            users = db.query(User).filter(User.deleted_at == None).options(load_only(User.id, User.name, User.surname, User.email, User.mobile_no, User.city, User.state, User.country)).all()
            base_url = os.getenv("BASE_URL")
            img_url = f"{base_url}"
            user_data = [
            {
                "ID": u.id,
                "Name": u.name,
                "Surname": u.surname,
                "Email": u.email,
                "Profile Picture": os.path.join(img_url, u.profile_image) if u.profile_image else None,
                "Mobile No": u.mobile_no,
                "City": u.city,
                "State": u.state,
                "Country": u.country
            } for u in users
        ]

            df = pd.DataFrame(user_data)
      

            # Create output directory
            output_dir = os.path.join(os.getcwd(), "uploads", "excel")
            os.makedirs(output_dir, exist_ok=True)
            os.chmod(output_dir, 0o777)

            # Timestamped filename
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.xlsx"
            output_path = os.path.join(output_dir, filename)

            df.to_excel(output_path, index=False)
            db.close()

            # Build public URL using BASE_URL env
            file_url = f"{base_url}uploads/excel/{filename}"

            return {"path": file_url}

        except Exception as e:
                traceback_str = traceback.format_exc()
                print(traceback_str)
    
                line_no = traceback.extract_tb(e.__traceback__)[-1][1]
                print(f"Exception occurred on line {line_no}")
                return str(e) 
        
    def upload_excel(request: Request,background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(getDb)):
        try:
            user_id = GeneralHelper.get_token(request, db)
            user_roles = db.query(UserHasRoles.role_id).filter(UserHasRoles.user_id == user_id).all()
            roles_list = [role.role_id for role in user_roles]

            # Check if role_id 1 exists
            if 1 in roles_list:
                output_dir = os.path.join(os.getcwd(), "uploads", "uploaded_excel")

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                    os.chmod(output_dir, 0o777)
                    
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                file_name = f"excel_{timestamp}.xlsx"

                file_loc = f"{output_dir}/{file_name}"
                with open(file_loc, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)

                dataframe = pd.read_excel(file_loc)

                already_exists = []

                for index, row in dataframe.iterrows():
                    row.to_dict()
                    check_user = db.query(User).filter(User.email == row['email'], User.deleted_at == None).first()
                    password = GeneralHelper.generate_random_password()

                    if check_user is None:
                        user = User(
                            name = row['name'],
                            surname = row['surname'],
                            email = row['email'],
                            password = hash_(password),
                            profile_image = "uploads\default.jpg",
                            mobile_no = row['mobile_no'],
                            city = row['city'],
                            state = row['state'],
                            country = row['country']
                        )

                        db.add(user)
                        db.commit()
                        db.refresh(user)

                        check_user = db.query(User).filter(User.email == row['email']).first()

                        background_tasks.add_task(GeneralHelper.send_password_email, user.name, user.surname, password, user.email, background_tasks)

                        user_has_role = UserHasRoles(
                            user_id = user.id,
                            role_id = 5  # Default to role_id 1 if not provided
                            )

                        db.add(user_has_role)
                        db.commit()

                    else:
                        already_exists.append(row['email'])
                
                os.remove(file_loc)

                if already_exists == []:
                    return True
                else:
                    exists_emails = ", ".join(already_exists)
                    exists = {"These users already exist": exists_emails}
                    return exists

            else:
                return False
            
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
 
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e)
        
    def delete(id: int, db: Session = Depends(getDb)):
        try:
            user = db.query(User).filter(User.id == id, User.deleted_at != None).first()
            if not user:
                return False
            else:
                user.deleted_at = datetime.now(timezone.utc)
                db.commit()
                return True

        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
 
            line_no = traceback.extract_tb(e.__traceback__)[-1][1]
            print(f"Exception occurred on line {line_no}")
            return str(e) 