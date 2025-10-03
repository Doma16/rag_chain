from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, SQLModel

from database import (
    User,
    UserPayLoad,
    UserQuery,
    get_engine,
    get_session,
    get_user_by_username,
)
from document import router as document_router
from jwt import create_token, read_token

app = FastAPI(on_startup=[lambda: SQLModel.metadata.create_all(get_engine())])
templates = Jinja2Templates("app/templates")

app.include_router(document_router)


@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=JSONResponse)
def register(user: UserQuery, session: Session = Depends(get_session)):
    if get_user_by_username(session, user.username):
        return JSONResponse(
            status_code=404, content={"detail": "Username exists. Try different one."}
        )

    db_user = User(username=user.username, password=hash_password(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return JSONResponse(
        status_code=200,
        content={"detail": "Sucess! \n You are now being redirected to home page!"},
    )


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=JSONResponse)
def login(
    form: UserQuery,
    session: Session = Depends(get_session),
):
    user = get_user_by_username(session, form.username)
    if not user or not user.password == hash_password(form.password):
        return JSONResponse(
            status_code=404, content={"detail": "Invalid username or password."}
        )

    token = create_token({"username": user.username})

    response = JSONResponse(
        status_code=200,
        content={
            "detail": "Sucess! \n You are now being redirected to home page!",
        },
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
    )

    return response


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    token = request.cookies.get("access_token")
    blank_welcome = templates.TemplateResponse(
        "index.html", {"request": request, "message": "Welcome!"}
    )
    if not token:
        return blank_welcome
    token_decoded = read_token(token)
    if not token_decoded:
        return blank_welcome
    
    payload = UserPayLoad(**token_decoded)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "message": f"Welcome {payload.username}!",
            "payload": payload,
        },
    )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.post("/logout", response_class=JSONResponse)
def logout():
    response = JSONResponse(
        status_code=200,
        content={
            "detail": "Sucess! \n You are now being redirected to home page!",
        },
    )
    response.delete_cookie("access_token", secure=False, httponly=True, samesite="lax")
    return response

def hash_password(password: str):
    """Dummy password hash."""
    return password
