
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="super_secret_key")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class Member(BaseModel):
    username: str
    password: str

user_db = {
    "Bob": Member(username="Bob", password="1234"),
    "test": Member(username="test", password="test")
}



async def get_session(request: Request):
    session = request.session
    session.setdefault("SIGNED-IN", False)
    return session


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request, session: dict = Depends(get_session)):
    if session["SIGNED-IN"] == True:
        return RedirectResponse(url="/member", status_code=303)
    
    return templates.TemplateResponse(request=request, name="signin.html")

@app.get("/signin", response_class=HTMLResponse)
async def signin(request: Request, session: dict = Depends(get_session)):

    if session["SIGNED-IN"] == True:
        return RedirectResponse(url="/member", status_code=303)
    
    return templates.TemplateResponse(request=request, name="signin.html")

@app.post("/signin", response_class=HTMLResponse)
async def process_login(request: Request, member: Member = Depends(Member), session: dict = Depends(get_session)): 

    if member.username in user_db and user_db[member.username].password == member.password:
        logging.info(f"Session data: {session}")
        #add session: sign in
        session["SIGNED-IN"] = True
        session["username"] = member.username
        return RedirectResponse(url="/member", status_code=303)
    
    if not member.username or not member.password:
        raise HTTPException(status_code=400, detail="帳號或密碼不能為空")

    if member.username not in user_db or user_db[member.username].password != member.password:
        raise HTTPException(status_code=401, detail="帳號或密碼輸入錯誤")

    

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request, session: dict = Depends(get_session)):
    # signed_in = session.get("SIGNED-IN", False)
    # if not signed_in:
    if session["SIGNED-IN"] == True:
        return templates.TemplateResponse(request=request, name="member.html", context={"username": session.get("username")})
        
    return RedirectResponse(url="/", status_code=303)

    

@app.get("/error", response_class=HTMLResponse)
async def error(request: Request):
    return templates.TemplateResponse(request=request, name="error.html")

@app.get("/signout", response_class=HTMLResponse)
async def signout(request: Request, session: dict = Depends(get_session)):
    session["SIGNED-IN"] = False
    return RedirectResponse(url="/", status_code=303)
