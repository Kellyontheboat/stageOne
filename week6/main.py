from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from typing import Optional, List, Tuple

import mysql.connector.pooling
#import pdb
import os

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="super_secret_key")
static_dir = os.path.join(os.path.dirname(__file__), "static")

# Mount the static directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory="templates")

# Connect to MySQL database
dbconfig = {
    "user": "root",
    "password": "password",
    "host": "127.0.0.1",
    "database": "website"
}

conn_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)
print("Connected to MySQL database")

def get_connection():
    return conn_pool.get_connection()


def execute_query(query, params=Tuple, commit=False) -> Tuple[List[Tuple], List[str]]:
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(query, params)
    # Get column_names = ['id', 'name', 'username', 'password', 'follower_count', 'time']
    column_names = [desc[0] for desc in cursor.description]
    # commit flag indicate whether the current operation requires committing the transaction to the database
    # delete,update,insert commit change to db and typically do not return meaningful results like select queries do
    # If commit is True, indicating that the operation was an insert, update, or delete operation, result is set to None because there is no meaningful result to return in these cases.
    if commit:
        con.commit()
    result = cursor.fetchall() if not commit else None
    cursor.close()
    con.close()
    return result, column_names

def authenticate_user(username: str, password: str):
    query = "SELECT * FROM member WHERE username = %s AND password = %s"
    return execute_query(query, (username, password))


def check_existing_username(username: str):
    query = "SELECT * FROM member WHERE username = %s"
    return execute_query(query, (username,))

def insert_new_user(name: str, username: str, password: str):
    insert_query = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    execute_query(insert_query, (name, username, password), commit=True)
class Member(BaseModel):
    #id: int
    name: str
    username: str
    password: str
    #follower_count: int
    #time: str 


async def get_session(request: Request):
    session = request.session
    session.setdefault("SIGNED-IN", False)
    return session


@app.get("/", response_class=HTMLResponse, name="home")
async def homepage(request: Request, session: dict = Depends(get_session)):

    if session["SIGNED-IN"]:
        return RedirectResponse(url="/member", status_code=303)
    
    return templates.TemplateResponse(request=request, name="signin.html")


@app.post("/signin", response_class=HTMLResponse, name="signin")
async def process_login(request: Request, username: str = Form(None), password: str = Form(None), session=Depends(get_session)):

    if not username or not password:
        error_message = "帳號或密碼不能為空"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    # Authenticate user from database
    user_data, column_names = authenticate_user(username, password)

    
    if not user_data:
        error_message = "帳號或密碼輸入錯誤"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    for i, column_name in enumerate(column_names):
            # Exclude the 'time' column
            if column_name == 'time':
                continue
            # there is only one user login a time, so we can use index 0
            #write the user data to the session
            session[column_name] = user_data[0][i]
        
    request.session["SIGNED-IN"] = True
    # request.session["username"] = username
    # request.session["name"] = user_name
    # session {'SIGNED-IN': True, 'username': 'test', 'id': 1, 'name': 'test2', 'password': 'test', 'follower_count': 10}
    print("session", request.session)
    return RedirectResponse(url="/member", status_code=303)
    

@app.post("/signup", response_class=HTMLResponse, name="signup")
async def process_signup(request: Request, signup_name: str = Form(None), signup_username: str = Form(None), signup_password: str = Form(None)):
    if not signup_username or not signup_username or not signup_password:
        # error_message = "姓名、帳號或密碼不能為空"
        # return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
        return RedirectResponse(url="/", status_code=303)
    
    # Check if username already exists
    existing_user = check_existing_username(signup_username)
    if existing_user:
        error_message = "Repeated username"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

    # Insert new user data into the member table
    insert_new_user(signup_name, signup_username, signup_password)

    # Redirect to the home page
    return RedirectResponse(url="/", status_code=303)


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
    # Clear the session data
    # Clear all data in the session
    session.clear()
    # Redirect to the home page
    return RedirectResponse(url="/", status_code=303)

@app.get("/square/{enter_int}", response_class=HTMLResponse, name="square")
async def square_result(request: Request, enter_int: Optional[int] = None):
    if enter_int is not None:
        return templates.TemplateResponse("square_result.html", {"request": request, "square": enter_int ** 2})
    else:
        return templates.TemplateResponse("square_form.html", {"request": request, "enter_int": None})
