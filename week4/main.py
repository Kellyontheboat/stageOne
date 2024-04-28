from fastapi import FastAPI, Request, Form, Depends, HTTPException
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
    "Bob": "1234",
    "test": "test"
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

@app.get("/square", response_class=HTMLResponse)
async def square(request: Request, enter_int: str = Form(...)):
    if enter_int is not None:
            
            return RedirectResponse(url="/square/{enter_int}", status_code=303)
    else:
            return RedirectResponse(url="/", status_code=303)


@app.post("/square", response_class=HTMLResponse)
async def get_int(request: Request, enter_int: str = Form(...)):
    if enter_int.isdigit():
        return RedirectResponse(url=f"/square/{enter_int}", status_code=303)
    else:
        RedirectResponse(url="/", status_code=303)

@app.get("/square/{enter_int}", response_class=HTMLResponse, name="square")
async def square(request: Request, enter_int: int):
    # print(f"Received enter_int: {enter_int}") # Debugging line
    # try:
    #     enter_int = int(enter_int)
    # except ValueError as e:
    #     print(f"Error converting enter_int to int: {e}") # Debugging line
    #     # Handle the error, e.g., by returning an error response
    #     return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})
    if enter_int:
        return templates.TemplateResponse("square_result.html", {"request": request, "square": enter_int**2})
    else:
        # Handle the case where enter_int is empty or invalid
        return RedirectResponse(url="/", status_code=303)

# @app.post("/square", response_class=HTMLResponse)
# async def get_int(request: Request, enter_int: str = Form(...)):
#     if enter_int.isdigit():  # Check if the input is a valid integer
#         return RedirectResponse(url=f"/square/{enter_int}", status_code=303)
#     else:
#         raise HTTPException(status_code=400, detail="Please enter a valid integer value")
    