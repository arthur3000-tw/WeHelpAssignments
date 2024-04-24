# 載入資料庫
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated, Optional
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()

# 將靜態資料擺放於 static 資料夾中
app.mount("/static", StaticFiles(directory="static"), name="static") 

# 使用 Jinja2 將要導入的頁面指向 templates 資料夾中
templates = Jinja2Templates(directory="templates") 

# 加入 SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key="my-secret-key") 

# 帳號密碼
id_password = {"test" : "test"} 

# member頁面，確認使用者登入狀態，無登入導向 home.html，已登入導向 member.html
@app.get("/member", response_class=HTMLResponse)
async def index(request: Request):
    user = request.session.get("user")
    if not user:
        return templates.TemplateResponse(
            request=request, name="home.html"
        )
    return templates.TemplateResponse(
        request=request, name="member.html"
    )

# 首頁，將 / 的 endpoint 導向 home.html
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html"
    )

# 登入，收集 home.html 中的 username 及 password，進行確認，若有空值或帳號密碼錯誤，導入 error.html 並再後加上相對應 message 資訊
# 若為正確則導入 member.html，並將 session 中的 user 設定為 username
@app.post("/signin")
async def login(request:Request, username: Annotated[str|None, Form()] = None, password: Annotated[str|None, Form()] = None):
    if(username == None or password == None):
        return RedirectResponse("/error" + "?message=請輸入帳號或密碼", status_code=status.HTTP_303_SEE_OTHER)
    elif (username not in id_password):
        return RedirectResponse("/error" + "?message=帳號或密碼錯誤", status_code=status.HTTP_303_SEE_OTHER)
    elif (id_password[username] == password):
        request.session["user"] = username
        return RedirectResponse("/member", status_code=status.HTTP_303_SEE_OTHER)
    elif (id_password[username] != password):
        return RedirectResponse("/error" + "?message=帳號或密碼錯誤", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse("/home.html", status_code=status.HTTP_303_SEE_OTHER)

# 登出，將 Session 中的 user 設定為 None
@app.get("/signout")
async def logout(request:Request):
    request.session["user"] = None
    return templates.TemplateResponse(
        request=request, name="home.html"
    )

# 錯誤頁面處理，取得 message 資訊，傳入 error.html 中，頁面顯示 message 資訊
@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str | None):
    return templates.TemplateResponse(
        request=request, name="error.html", context={"message": message}
    )

# 正整數平方，收集 home.html 中的 number，導入 /square/{number} 頁面
@app.post("/square")
async def square(request: Request, number: Annotated[int, Form()]):
    return RedirectResponse("/square/" + str(number), status_code=status.HTTP_303_SEE_OTHER)

# 正整數平方，取得 number，傳入 square.html 中，頁面顯示平方後結果資訊
@app.get("/square/{number}", response_class=HTMLResponse)
async def index(request: Request, number: int):
    return templates.TemplateResponse(
        request=request, name="square.html", context={"number":number}
    )