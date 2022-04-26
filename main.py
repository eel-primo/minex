from typing import Optional
import uuid
import xmlparser
from fastapi import FastAPI, Request, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from data.base import crud, models, schemas
from data.base.db import SessionLocal, engine

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

NEWS = xmlparser.open_news()
print(NEWS.get("post"))


app = FastAPI(debug=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home(request: Request, action: Optional[str] = None, db: Session = Depends(get_db)):
    userid = request.cookies.get("uuid")
    err = ""
    if action == "login":
        if request.headers.get("error") is not None:
            err = request.headers.get("error")
        return templates.TemplateResponse("login.html", {"request": request, "data": {"server_count": crud.count_servers(db), "hidden": True, "error": err}})
    if userid is None:
        return templates.TemplateResponse("news.html", {"request": request, "data": {"server_count": crud.count_servers(db), "authorized": False, "news": NEWS.get("post")}})
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": {"server_count": crud.count_servers(db), "authorized": True, "user_id": userid, "servers":{}}})


@app.get("/auth/save-session", response_class=HTMLResponse)
async def save_session(request: Request):
    response = RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
    response.delete_cookie("uuid")
    return response

@app.post("/auth/load-session")
async def load_session(request: Request,db: Session = Depends(get_db)):
    x = await request.form()
    db_user = crud.get_user(db, user_uuid=x.get("uuid"))
    if not db_user:
        response = RedirectResponse(url="/?action=login",status_code=status.HTTP_302_FOUND, headers={"error": "ID not found!"})
        return response
    # a82d62e4-be8d-4337-94da-08153ea897e1

    response = RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
    response.set_cookie("uuid", x.get("uuid"))
    return response

@app.get("/auth/create-session")
async def create_session(db: Session = Depends(get_db)):
    userid = str(uuid.uuid4())
    db_user = crud.get_user(db, user_uuid=userid)
    if db_user:
        return RedirectResponse('/auth/load-session',status_code=status.HTTP_302_FOUND)
    user_model = schemas.UserCreate
    user_model.uuid = userid
    crud.create_user(db=db, user=user_model)
    response = RedirectResponse(url="/",status_code=status.HTTP_302_FOUND)
    response.set_cookie("uuid", userid)
    return response
