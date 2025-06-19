from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from app.models import user_model
from config.database import engine
from app.modules.users import user_route
from app.modules.login import login_route

app = FastAPI()

user_model.Base.metadata.create_all(engine)

app.include_router(login_route.router)
app.include_router(user_route.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)