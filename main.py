from fastapi import FastAPI, Depends, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from sqlmodel import SQLModel, Session

from jwt import create_token
from database import get_engine, UserCreate, get_user_by_username, User, Token

engine = get_engine()
app = FastAPI(on_startup=[lambda: SQLModel.metadata.create_all(engine)])
templates = Jinja2Templates("templates")


def _get_session():
    with Session(engine) as session:
        return session


# @app.get("/insert")
# @app.get("/query")


@app.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register", response_class=JSONResponse)
def register(user: UserCreate, session: Session = Depends(_get_session)):
    if get_user_by_username(session, user.username):
        return JSONResponse(
            status_code=404, content={"detail": "Username exists. Try different one."}
        )

    db_user = User(username=user.username, password=user.password)
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
    form: UserCreate,
    session: Session = Depends(_get_session),
):
    user = get_user_by_username(session, form.username)
    if not user or not user.password == form.password:
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

    return templates.TemplateResponse(
        "index.html", {"request": request, "message": "Welcome"}
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
    response.delete_cookie("access_token")
    return response
