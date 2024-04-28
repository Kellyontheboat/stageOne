from fastapi import FastAPI, Request, Form, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from typing import Optional

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="super_secret_key")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class Member(BaseModel):
    username: str
    password: str 

user_db = {
    "Bob": "1234",
    "test": "test"
}

async def get_session(request: Request):
    session = request.session
    session.setdefault("SIGNED-IN", False)
    return session


@app.get("/", response_class=HTMLResponse, name="home")
async def homepage(request: Request, session: dict = Depends(get_session)):

    if session["SIGNED-IN"] == True:
        return RedirectResponse(url="/member", status_code=303)
    
    return templates.TemplateResponse(request=request, name="signin.html")


@app.post("/signin", response_class=HTMLResponse, name="signin")
async def process_login(request: Request, username: str = Form(None), password: str = Form(None)):

    
    if not username or not password:
        error_message = "帳號或密碼不能為空"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
    
    if username not in user_db or password != user_db[username]:
        error_message = "帳號或密碼輸入錯誤"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
        
        
    
    if username in user_db and password == user_db[username]:
        request.session["SIGNED-IN"] = True
        request.session["username"] = username
        return RedirectResponse(url="/member", status_code=303)
    
    
    

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request, session: dict = Depends(get_session)):
    # signed_in = session.get("SIGNED-IN", False)
    # if not signed_in:
    if session["SIGNED-IN"] == True:
        return templates.TemplateResponse(request=request, name="member.html", context={"username": session.get("username")})
        
    return RedirectResponse(url="/", status_code=303)
 
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str = None):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get("/signout", response_class=HTMLResponse)
async def signout(request: Request, session: dict = Depends(get_session)):
    session["SIGNED-IN"] = False
    return RedirectResponse(url="/", status_code=303)

@app.get("/square/{enter_int}", response_class=HTMLResponse, name="square")
async def square_result(request: Request, enter_int: Optional[int] = None):
    if enter_int is not None:
        # If enter_int is provided, calculate the square and render the result
        return templates.TemplateResponse("square_result.html", {"request": request, "square": enter_int ** 2})
    else:
        # If enter_int is not provided, render the form with enter_int set to None
        return templates.TemplateResponse("square_form.html", {"request": request, "enter_int": None})
