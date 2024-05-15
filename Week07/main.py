from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector


app = FastAPI()

# 將靜態資料擺放於 static 資料夾中，藉由 mount 方法取得位置並讀取檔案
app.mount("/static", StaticFiles(directory="static"), name="static")

# 使用 Jinja2 將要導入的頁面從 templates 資料夾中讀取
templates = Jinja2Templates(directory="templates")

# 加入 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="my-secret-key")

# 加入 CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 建立 Data 資料 model
class Data(BaseModel):
    id: int
    name: str
    username: str


# 建立 Response 資料 model
class myResponse(BaseModel):
    data: Data = None


# 建立 UpdateName 資料 model
class UpdateName(BaseModel):
    name: str


# 連線 Database 資訊
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="mywebsite"
)
mycursor = mydb.cursor(dictionary=True)


# 確認帳號密碼 checkSignIn(username, password)
# 輸入
# str: username              帳號
# str: password              密碼
# 輸出 list [status, ...]
# list: [1]                  表示沒有這個使用者
# list: [2, name, id]        表示密碼正確，並且回傳 name、id
# list: [3]                  表示密碼錯誤
# list: [4]                  表示其他狀況
def checkSignIn(username, password):
    # 確認是否有此帳號
    # 從資料庫中的 members 搜尋 username
    command = "SELECT * FROM members WHERE username = %s"
    val = (username, )
    mycursor.execute(command, val)
    # 取得結果
    myresult = mycursor.fetchall()
    # 確認結果
    # 沒有 username
    if (len(myresult) == 0):
        return [1]  # 沒有這個使用者
    # 有一筆 username
    elif (len(myresult) == 1):
        # 確認密碼
        # 密碼正確
        if (myresult[0]["password"] == password):
            # 密碼正確，並且回傳 name、id
            return [2, myresult[0]["name"], myresult[0]["id"]]
        # 密碼錯誤
        else:
            return [3]  # 密碼錯誤
    # 其他狀況
    else:
        return [4]  # 其他狀況


# 註冊帳號密碼 memberSignUp(name, username, password)
# 輸入
# str: name              使用者名稱
# str: username          使用者帳號
# str: password          使用者密碼
# 輸出 list[status]
# list: [1]              註冊完成
# list: [2]..............username 重複
def memberSignUp(name, username, password):
    # 確認 username 是否存在
    # 從資料庫中的 members 搜尋 username
    command = "SELECT * FROM members WHERE username = %s"
    val = (username, )
    mycursor.execute(command, val)
    # 取得結果
    myresult = mycursor.fetchall()
    # 確認結果
    # 沒有 username
    if (len(myresult) == 0):
        command = "INSERT INTO members (name, username,password) VALUES (%s,%s,%s)"
        val = (name, username, password)
        mycursor.execute(command, val)
        mydb.commit()
        return [1]  # 註冊完成
    # 有 username
    else:
        return [2]  # username 重複


# 新增留言 addMessage(message)
# 輸入
# str: id
# str: message
def addMessage(id, message):
    command = "INSERT INTO messages (members_id, content) VALUES (%s ,%s)"
    val = (id, message)
    mycursor.execute(command, val)
    mydb.commit()
    return


# 取得留言 getMessage()
# 輸出
# list: result     members 中的 name、messages 中的 content 及 id 依據時間先後排序
def getMessage():
    command = "SELECT members.name, content, messages.id FROM messages JOIN members ON messages.members_id = members.id ORDER BY messages.time DESC"
    mycursor.execute(command)
    result = mycursor.fetchall()
    return result


# 刪除留言 removeMessage(user_id,message_id)
# 輸入
# str: user_id             members 中的 id
# str: message_id          messages 中的 id
# 輸出 list[status]
# list: [1]                刪除完成
# list: [2]..............  刪除失敗或其他狀況
def removeMessage(user_id, message_id):
    command = "DELETE FROM messages WHERE members_id = %s AND id = %s"
    val = (user_id, message_id)
    mycursor.execute(command, val)
    mydb.commit()
    # 刪除成功
    if mycursor.rowcount == 1:
        return [1]
    # 刪除失敗或其他狀況
    else:
        return [2]


# 刪除使用者 removeMember(username)
# 輸入
# str: username     使用者帳號
def removeMember(username):
    command = "DELETE FROM members WHERE username = %s"
    val = (username,)
    mycursor.execute(command, val)
    mydb.commit()
    return


# 修改使用者姓名 modifyName(username, changeName)
# 輸入
# str: username         使用者帳號
# str: changeName       要修改的姓名
# obj: request          Request物件
# 輸出
# {"ok": True}          修改成功
# {"error": True}       修改失敗
def modifyName(username, changeName, request):
    command = "UPDATE members SET name = %s WHERE username = %s"
    val = (changeName, username)
    mycursor.execute(command, val)
    mydb.commit()
    if (mycursor.rowcount == 1):
        request.session["name"] = changeName
        return {"ok": True}
    else:
        return {"error": True}


# 查詢使用者姓名 searchUsername(username)
# 輸入
# str: username           使用者帳號
# 輸出
# myResponse: myResponse(data=Data model)   myResponse 格式
def searchUsername(username):
    command = "SELECT id, name, username FROM members WHERE username = %s"
    val = (username,)
    mycursor.execute(command, val)
    myresult = mycursor.fetchall()
    if (len(myresult) == 1):
        # 有找到 username，回傳 myResponse(data = myresult[0]) 資訊
        return myResponse(data=Data.model_validate(myresult[0]))
    else:
        # 沒找到 username 或其他狀況，回傳 myResponse(data = null) 資訊
        return myResponse()


# 首頁 Home Page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


# 錯誤頁面 Error Page
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str | None):
    return templates.TemplateResponse(
        request=request, name="error.html", context={"message": message}
    )


# 登入 Signin Endpoint
@app.post("/signin")
async def signin(request: Request, username: Annotated[str | None, Form()] = None, password: Annotated[str | None, Form()] = None):
    # 確認帳號密碼
    result = checkSignIn(username, password)
    # 帳號不存在
    if (result[0] == 1):
        return RedirectResponse("/error" + "?message=帳號或密碼錯誤", status_code=status.HTTP_303_SEE_OTHER)
    # 密碼錯誤
    elif (result[0] == 3):
        return RedirectResponse("/error" + "?message=帳號或密碼錯誤", status_code=status.HTTP_303_SEE_OTHER)
    # 密碼正確，登入頁面
    elif (result[0] == 2):
        request.session["username"] = username  # 將 username 存入 session
        request.session["name"] = result[1]  # 將 name 存入 session
        request.session["id"] = result[2]  # 將 id 存入 session
        return RedirectResponse("/member", status_code=status.HTTP_303_SEE_OTHER)
    # 其他狀況，導至首頁
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


# 會員頁面 Member Page
@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    # 確認狀態
    username = request.session.get("username")  # 從 session 中取得 username
    # 未登入狀態
    if not username:
        return RedirectResponse("/",  status_code=status.HTTP_303_SEE_OTHER)
    # 登入狀態
    else:
        name = request.session.get("name")  # 從 session 中取得 name
        result = getMessage()
        return templates.TemplateResponse(
            request=request, name="member.html", context={"name": name, "result": result}
        )


# 會員登出 Signout Endpoint
@app.get("/signout")
async def signout(request: Request):
    request.session["username"] = None  # 將 session 中的 username 設定為 None
    request.session["name"] = None  # 將 session 中的 name 設定為 None
    return RedirectResponse("/",  status_code=status.HTTP_303_SEE_OTHER)


# 註冊會員 Signup Endpoint
@app.post("/signup")
async def signup(name: Annotated[str | None, Form()] = None, username: Annotated[str | None, Form()] = None, password: Annotated[str | None, Form()] = None):
    # 確認註冊狀況
    result = memberSignUp(name, username, password)
    # 註冊完成
    if (result[0] == 1):
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    # username 重複
    elif (result[0] == 2):
        return RedirectResponse("/error" + "?message=帳號已使用，請更換帳號！", status_code=status.HTTP_303_SEE_OTHER)
    # 其他狀況
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


# 會員留言 CreateMessage Endpoint
@app.post("/createMessage")
async def createmessage(request: Request, message: Annotated[str | None, Form()] = None):
    # 確認狀態
    username = request.session.get("username")  # 從 session 中取得 username
    # 未登入的狀態
    if not username:
        return RedirectResponse("/",  status_code=status.HTTP_303_SEE_OTHER)
    # 登入狀態，進行留言
    else:
        id = request.session.get("id")
        addMessage(id, message)
        return RedirectResponse("/member", status_code=status.HTTP_303_SEE_OTHER)


# 留言刪除 DeleteMessage Endpoint
@app.post("/deleteMessage")
async def deletemessage(request: Request, messageID: Annotated[str | None, Form()] = None):
    # 確認狀態
    username = request.session.get("username")  # 從 session 中取得 username
    # 未登入的狀態
    if not username:
        return RedirectResponse("/",  status_code=status.HTTP_303_SEE_OTHER)
    # 登入狀態，進行留言
    else:
        id = request.session.get("id")
        result = removeMessage(id, messageID)
        # member_id 正確，進行留言刪除
        if (result[0] == 1):
            return RedirectResponse("/member", status_code=status.HTTP_303_SEE_OTHER)
        # member_id 錯誤或其他狀況，登出並回首頁
        else:
            request.session["username"] = None
            request.session["name"] = None
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


# 帳號刪除 DeleteMember Endpoint
@app.post("/deleteMember")
async def deletemember(request: Request, deletePassword: Annotated[str | None, Form()] = None):
    # 確認狀態
    username = request.session.get("username")  # 從 session 中取得 username
    # 未登入的狀態
    if not username:
        return RedirectResponse("/",  status_code=status.HTTP_303_SEE_OTHER)
    # 登入狀態，確認密碼
    else:
        result = checkSignIn(username, deletePassword)
        # 密碼錯誤，將使用者登出，並轉至密碼錯誤頁面
        if (result[0] == 3):
            request.session["username"] = None
            request.session["name"] = None
            return RedirectResponse("/error" + "?message=密碼錯誤", status_code=status.HTTP_303_SEE_OTHER)
        # 密碼正確，刪除使用者
        elif (result[0] == 2):
            request.session["username"] = None
            request.session["name"] = None
            removeMember(username)
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


# 姓名修改 ChangeName Endpoint
@app.post("/changeName")
async def changename(request: Request, changeName: Annotated[str | None, Form()] = None):
    # 確認狀態
    username = request.session.get("username")  # 從 session 中取得 username
    # 未登入的狀態
    if not username:
        return RedirectResponse("/",  status_code=status.HTTP_303_SEE_OTHER)
    # 登入狀態，姓名修改
    else:
        modifyName(username, changeName, request)
        return RedirectResponse("/member", status_code=status.HTTP_303_SEE_OTHER)


# 使用者帳號查詢 MemberQuery Endpoint
@app.get("/api/member")
async def memberQuery(request: Request, username):
    # 確認狀態
    checkUsername = request.session.get("username")  # 從 session 中取得 username
    # 未登入的狀態
    if not checkUsername:
         # 回傳 {"data":null}
        return myResponse()
    # 登入狀態，帳號查詢
    else:
        result = searchUsername(username)
        return result


# 使用者姓名更改 NameUpdate Endpoint
@app.patch("/api/member")
async def nameUpdate(request: Request, updateName: UpdateName):
    # 確認狀態
    checkUsername = request.session.get("username")  # 從 session 中取得 username
    # 未登入的狀態
    if not checkUsername:
        # 回傳 {"error": True}
        return {"error": True}
    # 登入狀態，使用者姓名更改
    else:
        result = modifyName(checkUsername, updateName.name, request)
        return result
