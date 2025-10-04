from fastapi import APIRouter, Depends, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Session
from fastapi.templating import Jinja2Templates

from rag import process_query, split_document, add_document

from database import (
    get_session,
    DocumentQuery,
    Document,
    QueryString,
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

    return templates.TemplateResponse(
        "upload.html", context={"request": request, "username": user.username}
    )


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

    docs = split_document(doc.content)
    for doc in docs:
        doc.metadata["doc_id"] = db_doc.id
        add_document(user.id, doc)

    return JSONResponse(
        status_code=200,
        content={
            "detail": "Document uploaded! \n You are now being redirected to documents page!",
            "message": f"User {user.username} uploaded a doc!",
        },
    )


@router.get("/d/{doc_id}")
def get_doc_id(
    request: Request,
    doc_id: int,
    start_index: int = Query(None, ge=0),
    start_length: int = Query(0, ge=0),
    session: Session = Depends(get_session),
):
    token = get_token_or_redirect(request)
    user = get_user(session, token)
    doc = get_document(session, doc_id)

    if user.id != doc.user_id:
        raise HTTPException(
            status_code=303, detail="Redirect", headers={"Location": "/documents"}
        )

    filename = doc.filename
    content = doc.content
    if start_index:
        end_index = start_index + start_length
        filename += f" From: {start_index} To: {end_index}"
        content = "...\n" + content[start_index:end_index] + "\n..."

    return templates.TemplateResponse(
        "doc_page.html",
        context={"request": request, "filename": filename, "content": content},
    )


@router.get("/query", response_class=HTMLResponse)
def query_doc(request: Request, session: Session = Depends(get_session)):
    token = get_token_or_redirect(request)
    user = get_user(session, token)

    return templates.TemplateResponse(
        "query_docs.html", context={"request": request, "username": user.username}
    )


@router.post("/query", response_class=JSONResponse)
async def query_doc_post(
    request: Request, query: QueryString, session: Session = Depends(get_session)
):
    token = get_token_or_redirect(request)
    user = get_user(session, token)

    response, docs = await process_query(user.id, query.query)

    return JSONResponse(
        status_code=200,
        content={
            "response": response,
            "docs": [
                (
                    f"{idx}. {doc.page_content[:10]}...",
                    doc.metadata["doc_id"],
                    doc.metadata["start_index"],
                    len(doc.page_content),
                )
                for idx, doc in enumerate(docs)
            ],
        },
    )
