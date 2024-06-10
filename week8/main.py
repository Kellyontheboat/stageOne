from fastapi import FastAPI

app = FastAPI()
message = "Hello World"
@app.get("/")
def root():
    return {"message": message}

# from fastapi import FastAPI, Request, Form, Depends, HTTPException
# from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
# from fastapi.exceptions import RequestValidationError
# from starlette.exceptions import HTTPException as StarletteHTTPException
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel
# from starlette.middleware.sessions import SessionMiddleware
# from starlette.requests import Request
# from typing import Optional, List, Tuple
# import pdb
# import json

# import mysql.connector.pooling
# import os

# app = FastAPI()

# app.add_middleware(SessionMiddleware, secret_key="super_secret_key")
# static_dir = os.path.join(os.path.dirname(__file__), "static")

# # Mount the static directory
# app.mount("/static", StaticFiles(directory=static_dir), name="static")
# templates = Jinja2Templates(directory="templates")

# # Connect to MySQL database
# dbconfig = {
#     "user": "root",
#     "password": "password",
#     "host": "127.0.0.1",
#     "database": "website"
# }

# conn_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)
# print("Connected to MySQL database")

# def get_connection():
#     return conn_pool.get_connection()


# def execute_query(query, params: Tuple = (), commit: bool = False) -> Tuple[List[dict], List[str]]:
#     con = get_connection()
#     cursor = con.cursor(dictionary=True) # Create a cursor with dictionary=True
#     cursor.execute(query, params)
    
#     # commit flag indicate whether the current operation requires committing the transaction to the database
#     # delete,update,insert commit change to db and typically do not return meaningful results like select queries do
#     # If commit is True, indicating that the operation was an insert, update, or delete operation, result is set to None because there is no meaningful result to return in these cases.
#     if commit:
#         con.commit()
#         result = None
#         column_names = None
    
#     else:
#         result = cursor.fetchall()  # Fetch all rows as dictionaries
#         #column_names = [desc[0] for desc in cursor.description]
    
#     cursor.close()
#     con.close()
#     return result   #, column_names

# def authenticate_user(username: str, password: str):
#     query = "SELECT * FROM member WHERE username = %s AND password = %s"
#     return execute_query(query, (username, password))


# def check_existing_username(username: str):
#     query = "SELECT * FROM `member` WHERE username = %s"
#     return execute_query(query, (username,))

# def insert_new_user(name: str, username: str, password: str):
#     insert_query = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
#     return execute_query(insert_query, (name, username, password), commit=True)

# def insert_message(member_id: int, content:str):
#     insert_query = "INSERT INTO `message` (member_id, content) VALUES (%s, %s)"
#     return execute_query(insert_query, (member_id, content), commit=True)

# def delete_message_from_db(message_id: int):
#     delete_query = "DELETE FROM `message` WHERE id = %s"
#     return execute_query(delete_query, (message_id,), commit=True)

# def join_member_message():
#     join_query = "SELECT * FROM `message` JOIN `member` ON message.member_id = member.id"
#     return execute_query(join_query)

# def find_message_member_id(message_id: int):
#     query = "SELECT member_id FROM `message` WHERE message.id = %s"
#     return execute_query(query, (message_id,))

# def find_member_by_username(username: str):
#     query = "SELECT * FROM `member` WHERE username = %s"
#     return execute_query(query, (username,))

# def update_member_name(new_name: str, user_id: int):
#     try:
#         query = "UPDATE `member` SET `name` = %s WHERE `id` = %s"
#         execute_query(query, (new_name, user_id), commit=True)
#         return True
#     except Exception as e:
#         print(f"Database update failed: {e}")
#         return False

# class Member(BaseModel):
#     #id: int
#     name: str
#     username: str
#     password: str
#     #follower_count: int
#     #time: str 

# class UpdateNameRequest(BaseModel):
#     name: str

# async def get_session(request: Request):
#     #pdb.set_trace()
#     session = request.session
#     session.setdefault("SIGNED-IN", False)
#     return session

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request: Request, exc: StarletteHTTPException):
#     if exc.status_code == 404:
#         return JSONResponse(status_code=404, content={"data": None})
#     else:
#         return JSONResponse(status_code=exc.status_code, content={"error": True})

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(status_code=422, content={"error": True})

# @app.exception_handler(Exception)  # Add this handler for general exceptions
# async def general_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={"error": True},
#     )

# @app.get("/", response_class=HTMLResponse, name="home")
# async def homepage(request: Request, session: dict = Depends(get_session)):

#     if session["SIGNED-IN"]:
#         return RedirectResponse(url="/member", status_code=303)
    
#     return templates.TemplateResponse(request=request, name="signin.html")

# @app.post("/signin", response_class=HTMLResponse, name="signin")
# async def process_login(request: Request, username: str = Form(None), password: str = Form(None), session=Depends(get_session)):

#     if not username or not password:
#         error_message = "帳號或密碼不能為空"
#         return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

#     # Authenticate user from database
#     user_data = authenticate_user(username, password)
    
#     pdb.set_trace()
#     session = user_data
    
#     if not user_data:
#         error_message = "帳號或密碼輸入錯誤"
#         return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

#     request.session["SIGNED-IN"] = True
#     print("session", request.session)
#     return RedirectResponse(url="/member", status_code=303)
    
# @app.post("/signup", response_class=HTMLResponse, name="signup")
# async def process_signup(request: Request, signup_name: str = Form(None), signup_username: str = Form(None), signup_password: str = Form(None)):
#     if not signup_name or not signup_username or not signup_password:
#         error_message = "姓名、帳號或密碼不能為空"
#         return RedirectResponse(url=f"/error?message={error_message}", status_code=303)
        
#     # Check if username already exists
#     existing_user = check_existing_username(signup_username)
#     if existing_user[0] != []:
#         error_message = "Repeated username"
#         return RedirectResponse(url=f"/error?message={error_message}", status_code=303)

#     # Insert new user data into the member table
#     insert_new_user(signup_name, signup_username, signup_password)

#     # Redirect to the home page
#     return RedirectResponse(url="/", status_code=303)

# @app.get("/member", response_class=HTMLResponse)
# async def member(request: Request, session: dict = Depends(get_session)): 
#     if session["SIGNED-IN"] == True:

#         messages = join_member_message()

#         # messages_list = []
#         # for message in messages:
#         #     message_id = message[0]
#         #     name = message[6]
#         #     content = message[2]
#         #     member_id = message[1]
#         #     messages_list.append((message_id, name, content, member_id))

#     #     return templates.TemplateResponse(request=request, name="member.html", context={"name": session.get("name"), "messages_list": messages_list})

#     # return RedirectResponse(url="/", status_code=303)

# @app.get("/api/member", response_class=JSONResponse)
# async def get_member(session: dict = Depends(get_session), username: str | None = None):# same as older version username: Optional[str] = None / username is the fetch url query parameter from js searchUser() 
#     if session["SIGNED-IN"] == True:

#         if username:
#             found_member = find_member_by_username(username)
#             # found_member:
#             # ([(4, 'Lily', 'Lily123', 'Lily456', 40, datetime.datetime(2024, 5, 7, 23, 4, 13))], 
#             #  ['id', 'name', 'username', 'password', 'follower_count', 'time'])

#             if not found_member[0]: 
#                 raise HTTPException(status_code=404)
        
#             # Convert the result_dict to a JSON string
#             return JSONResponse(status_code=200, content={
#                 "data": {
#                     "id": found_member[0][0][0],
#                     "name": found_member[0][0][1],
#                     "username": found_member[0][0][2]
#                 }
#             })
#         else:
#             raise HTTPException(status_code=400)       
    
#     raise HTTPException(status_code=401)

# @app.patch("/api/member", response_class=JSONResponse)
# # from the request body, get the UpdateNameRequest object(Pydantic model)
# async def update_member(update_name_req: UpdateNameRequest, session: dict = Depends(get_session)):

#     if session["SIGNED-IN"] == True:
        
#         new_name = update_name_req.name #from the request body, get the name value
#         try:
#             if update_member_name(new_name, session["id"]):
#                 session["name"] = new_name
#                 return JSONResponse(status_code=200, content={"ok": True})

#             else:
#                 raise HTTPException(status_code=500)
#         except Exception as e:
#             print(f"Error updating member name: {e}")
#             raise HTTPException(status_code=500)
    
#     raise HTTPException(status_code=401)

# @app.get("/error", response_class=HTMLResponse)
# async def error(request: Request, message: str = None):
#     return templates.TemplateResponse("error.html", {"request": request, "message": message})

# @app.get("/signout", response_class=HTMLResponse)
# async def signout(request: Request, session: dict = Depends(get_session)):
#     # Clear all data in the session
#     session.clear()
#     print("session", session)
#     # Redirect to the home page
#     return RedirectResponse(url="/", status_code=303)

# @app.post("/createMessage", response_class=HTMLResponse, name="createMessage")
# async def create_message(request: Request, message: str = Form(...), session: dict = Depends(get_session)):
#     if not session["SIGNED-IN"]:
#         return RedirectResponse(url="/", status_code=303)

#     # Insert the message into the message table
#     insert_message(session["id"], message)
#     return RedirectResponse(url="/member", status_code=303)

# @app.post("/deleteMessage", response_class=HTMLResponse, name="deleteMessage")
# async def delete_message(request: Request, message_id: int = Form(...), session: dict = Depends(get_session)):
#     if not session["SIGNED-IN"]:
#         return RedirectResponse(url="/", status_code=303)

#     message_member_id = find_message_member_id(message_id)[0][0][0] #([(5,)], ['member_id']) / use message_id to find the member_id
#     print("message_member_id", message_member_id)
#     if session["id"] == message_member_id:
#         delete_message_from_db(message_id)
#     # Delete the message from the message table
    
#     return RedirectResponse(url="/member", status_code=303)

# @app.get("/square/{enter_int}", response_class=HTMLResponse, name="square")
# async def square_result(request: Request, enter_int: Optional[int] = None): 
#     if enter_int is not None:
#         return templates.TemplateResponse("square_result.html", {"request": request, "square": enter_int ** 2})
#     else:
#         return templates.TemplateResponse("square_form.html", {"request": request, "enter_int": None})
