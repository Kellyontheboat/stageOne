from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from typing import Optional, List, Tuple

import mysql.connector.pooling
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


def execute_query(query, params: Tuple = (), commit=False) -> Tuple[List[Tuple], List[str]]:
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(query, params)
    
    # commit flag indicate whether the current operation requires committing the transaction to the database
    # delete,update,insert commit change to db and typically do not return meaningful results like select queries do
    # If commit is True, indicating that the operation was an insert, update, or delete operation, result is set to None because there is no meaningful result to return in these cases.
    if commit:
        con.commit()
    result = cursor.fetchall() if not commit else None
    # Get column_names = ['id', 'name', 'username', 'password', 'follower_count', 'time']
    column_names = [desc[0] for desc in cursor.description] if not commit else None
    # if not commit else None solve：column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    con.close()
    return result, column_names

def authenticate_user(username: str, password: str):
    query = "SELECT * FROM member WHERE username = %s AND password = %s"
    return execute_query(query, (username, password))


def check_existing_username(username: str):
    query = "SELECT * FROM `member` WHERE username = %s"
    return execute_query(query, (username,))

def insert_new_user(name: str, username: str, password: str):
    insert_query = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    return execute_query(insert_query, (name, username, password), commit=True)

def insert_message(member_id: int, content:str):
    insert_query = "INSERT INTO `message` (member_id, content) VALUES (%s, %s)"
    return execute_query(insert_query, (member_id, content), commit=True)

def delete_message_from_db(message_id: int):
    delete_query = "DELETE FROM `message` WHERE id = %s"
    return execute_query(delete_query, (message_id,), commit=True)

def join_member_message():
    join_query = "SELECT * FROM `message` JOIN `member` ON message.member_id = member.id"
    return execute_query(join_query)

def find_message_member_id(message_id: int):
    query = "SELECT member_id FROM `message` JOIN `member` ON message.member_id = member.id WHERE message.id = %s"
    return execute_query(query, (message_id,))

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

    #if user_data: store the user data in the session
    for i, column_name in enumerate(column_names):
            # Exclude the 'time' column
            if column_name == 'time':
                continue
        
            session[column_name] = user_data[0][i]
            # there is only one user login a time, so we can use index 0
            #write the user data to the session
            # session {'SIGNED-IN': True, 'username': 'test', 'id': 1, 'name': 'test2', 'password': 'test', 'follower_count': 10}
        
    request.session["SIGNED-IN"] = True
    print("session", request.session)
    return RedirectResponse(url="/member", status_code=303)
    
@app.post("/signup", response_class=HTMLResponse, name="signup")
async def process_signup(request: Request, signup_name: str = Form(None), signup_username: str = Form(None), signup_password: str = Form(None)):
    if not signup_name or not signup_username or not signup_password:
        error_message = "姓名、帳號或密碼不能為空"
        return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
        
    # Check if username already exists
    existing_user = check_existing_username(signup_username)
    if existing_user[0] != []:
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

        messages, column_names = join_member_message()

        messages_list = []
        for message in messages:
            message_id = message[0]
            name = message[6]
            content = message[2]
            member_id = message[1]
            messages_list.append((message_id, name, content, member_id))
        print(messages_list)

        return templates.TemplateResponse(request=request, name="member.html", context={"name": session.get("name"), "messages_list": messages_list})


    return RedirectResponse(url="/", status_code=303)
 
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str = None):
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.get("/signout", response_class=HTMLResponse)
async def signout(request: Request, session: dict = Depends(get_session)):
    # Clear all data in the session
    session.clear()
    print("session", session)
    # Redirect to the home page
    return RedirectResponse(url="/", status_code=303)

@app.post("/createMessage", response_class=HTMLResponse, name="createMessage")
async def create_message(request: Request, message: str = Form(...), session: dict = Depends(get_session)):
    if not session["SIGNED-IN"]:
        return RedirectResponse(url="/", status_code=303)

    # Insert the message into the message table
    insert_message(session["id"], message)
    return RedirectResponse(url="/member", status_code=303)

@app.post("/deleteMessage", response_class=HTMLResponse, name="deleteMessage")
async def delete_message(request: Request, message_id: int = Form(...), session: dict = Depends(get_session)):
    if not session["SIGNED-IN"]:
        return RedirectResponse(url="/", status_code=303)

    message_member_id = find_message_member_id(message_id)[0][0][0] #([(5,)], ['member_id'])
    print("message_member_id", message_member_id)
    if session["id"] == message_member_id:
        delete_message_from_db(message_id)
    # Delete the message from the message table
    
    return RedirectResponse(url="/member", status_code=303)

@app.get("/square/{enter_int}", response_class=HTMLResponse, name="square")
async def square_result(request: Request, enter_int: Optional[int] = None):
    if enter_int is not None:
        return templates.TemplateResponse("square_result.html", {"request": request, "square": enter_int ** 2})
    else:
        return templates.TemplateResponse("square_form.html", {"request": request, "enter_int": None})
