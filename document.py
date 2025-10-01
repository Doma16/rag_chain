from fastapi import APIRouter, Depends, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session
from fastapi.templating import Jinja2Templates

from database import (
    get_session,
    DocumentQuery,
    Document,
    get_user_documents,
    get_document,
)
from user import get_user

templates = Jinja2Templates("templates/documents")
router = APIRouter(prefix="/documents")


def get_token_or_redirect(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=303, detail="Redirect", headers={"Location": "/"}
        )
    return token


@router.get("", response_class=HTMLResponse)
def docs(
    request: Request,
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
):
    token = get_token_or_redirect(request)
    user = get_user(session, token)
    files = [(doc.filename, doc.id) for doc in get_user_documents(session, user.id)]
    total = len(files)
    start = (page - 1) * page_size
    end = start + page_size
    files = files[start:end]

    return templates.TemplateResponse(
        "docs.html",
        context={
            "request": request,
            "files": files,
            "page": page,
            "page_size": page_size,
            "total": total,
        },
    )


@router.get("/upload", response_class=HTMLResponse)
def upload_doc(request: Request, session: Session = Depends(get_session)):
    token = get_token_or_redirect(request)
    user = get_user(session, token)

    return templates.TemplateResponse("upload.html", context={"request": request})


@router.post("/upload", response_class=JSONResponse)
def upload_doc_post(
    request: Request, doc: DocumentQuery, session: Session = Depends(get_session)
):
    token = get_token_or_redirect(request)
    user = get_user(session, token)

    db_doc = Document(
        user_id=user.id,
        filename=doc.filename,
        content=doc.content,
    )
    session.add(db_doc)
    session.commit()
    session.refresh(db_doc)

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Document uploaded! \n You are now being redirected to documents page!",
            "message": f"User {user.username} uploaded a doc!",
        },
    )


@router.get("/{doc_id}")
def get_doc_id(request: Request, doc_id: int, session: Session = Depends(get_session)):
    token = get_token_or_redirect(request)
    user = get_user(session, token)
    doc = get_document(session, doc_id)

    if user.id != doc.user_id:
        raise HTTPException(
            status_code=303, detail="Redirect", headers={"Location": "/documents"}
        )

    return templates.TemplateResponse(
        "doc_page.html",
        context={"request": request, "filename": doc.filename, "content": doc.content},
    )


@router.get("/query", response_class=HTMLResponse)
def query_doc(): ...


@router.post("/query", response_class=JSONResponse)
def query_doc_post(): ...
