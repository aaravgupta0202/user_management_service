import base64
from datetime import datetime
import io
import shutil
from datetime import timezone
from jinja2 import Template
from PIL import Image
from fastapi import BackgroundTasks, Depends, Request, UploadFile
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
import os
from sqlalchemy.orm import Session
import jwt
from app.auth.auth_handler import ALGORITHM, SECRET_KEY
from app.auth.auth_handler import decodeJWT
from app.models.user_model import User
from app.templates import create_user_template
from app.templates import welcome_user_email
import random
import string
from config.database import getDb

class GeneralHelper:
    def send_email(name, surname, email, background_tasks: BackgroundTasks):
        conf = ConnectionConfig(
            MAIL_USERNAME = "nirbhay.verve@gmail.com",
            MAIL_PASSWORD = "xdjexcbtyvgkfdlu",
            MAIL_FROM = "reverlogy@gmail.com",
            MAIL_PORT = 465,
            MAIL_SERVER = "smtp.gmail.com",
            MAIL_FROM_NAME="Verve",
            MAIL_STARTTLS=False,       # Correct field
            MAIL_SSL_TLS=True,       # Correct field
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
            )

        body =  Template(create_user_template.email).render(name = name, surname = surname)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads/Attachment.pdf'))

        message = MessageSchema(
            subject= f"Hey {name}!",
            recipients=[email],
            body=body,
            subtype=MessageType.html,  # use MessageType.html for HTML emails
            attachments=[file_path]
            )

        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
        return {"message": "Email has been sent"}
    
    def send_password_email(name, surname, password, email, background_tasks: BackgroundTasks):
        conf = ConnectionConfig(
            MAIL_USERNAME = "nirbhay.verve@gmail.com",
            MAIL_PASSWORD = "xdjexcbtyvgkfdlu",
            MAIL_FROM = "reverlogy@gmail.com",
            MAIL_PORT = 465,
            MAIL_SERVER = "smtp.gmail.com",
            MAIL_FROM_NAME="Verve",
            MAIL_STARTTLS=False,       # Correct field
            MAIL_SSL_TLS=True,       # Correct field
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
            )

        body =  Template(welcome_user_email.email).render(name = name, surname = surname, password = password)
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads/Attachment.pdf'))

        message = MessageSchema(
            subject= f"Hey {name}!",
            recipients=[email],
            body=body,
            subtype=MessageType.html,  # use MessageType.html for HTML emails
            attachments=[file_path]
            )

        fm = FastMail(conf)
        background_tasks.add_task(fm.send_message, message)
        return {"message": "Email has been sent"}
    
    def UploadImage(upload_file: UploadFile):
        if upload_file:
            output_dir = os.path.join(os.getcwd(), "uploads")
            os.makedirs(output_dir, exist_ok=True)
            os.chmod(output_dir, 0o777)

            # Extract file extension
            filename_ext = upload_file.filename.split('.')[-1]

            # Generate a unique filename with timestamp
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}.{filename_ext}"
            output_path = os.path.join(output_dir, filename)

            # Save the file
            with open(output_path, "wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
            path = os.path.join("uploads", filename)
            return path
        
    def UploadImageBase64(base64_string):
        # If it includes a data URI prefix like 'data:image/png;base64,...', strip it
        if base64_string:
            output_dir = os.path.join(os.getcwd(), "uploads")
            if os.path.exists(output_dir):
                # Strip Data URI prefix if present
                if base64_string.startswith("data:image"):
                    base64_string = base64_string.split(",")[1]

                # Decode Base64 to bytes
                image_data = base64.b64decode(base64_string)

                # Use BytesIO to open image in memory
                image_stream = io.BytesIO(image_data)

                # Open image with Pillow
                image = Image.open(image_stream)
                extension = image.format.lower()
            

                # Generate filename with timestamp

                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}.{extension}"
                output_dir = os.path.join(os.getcwd(), "uploads")
                print("===========output_path=========", output_dir)
                os.makedirs(output_dir, exist_ok=True)
                os.chmod(output_dir, 0o777)  # Set permissions to allow writing
                
                output_path = os.path.join(output_dir, filename)
                
                # Save the image
                with open(output_path, "wb") as file:
                    file.write(base64.b64decode(base64_string))

                filename = os.path.join("uploads", filename)  # Return the relative path
                return filename
    
    def generate_random_password():
        length = 8
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(length))
        return password
    
    def get_token(request:Request, db: Session = Depends(getDb)):
        try:
            bearer_token = request.headers.get("Authorization")
            if bearer_token and bearer_token.startswith("Bearer "):
                bearer_token = bearer_token.split(" ")[1]
            else:
                raise Exception("Invalid or missing Authorization header")

            decoded_token = decodeJWT(bearer_token)
            user_id = decoded_token.get('user_id')
            return user_id
        except Exception as e:
            print(str(e))
            return False