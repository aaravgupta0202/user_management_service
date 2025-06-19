import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

MYSQL_URL = "mysql+pymysql://"+os.getenv("DB_USERNAME")+":"+os.getenv("DB_PASSWORD")+"@"+os.getenv("DB_HOST")+"/"+os.getenv("DB_DATABASE")
engine = create_engine(MYSQL_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def getDb():
    db = SessionLocal()
    try:
        yield db
    except Exception as ex:
        print("Error getting DB session : ", ex)
        raise 
    finally:
        db.close()

file = open(os.getcwd() + '/response_msg.json')
msg = json.load(file)
