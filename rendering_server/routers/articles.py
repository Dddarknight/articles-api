import os
from enum import Enum
from dotenv import load_dotenv

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from rendering_server.utils import templates
from rendering_server.utils import get_headers_with_token
from rendering_server.utils import get_login_redirect
from rendering_server.utils import api_request_get, api_request_put
from rendering_server.utils import api_request_post, api_request_delete
from rendering_server.utils import create_redirect_with_cookie


load_dotenv()

router = APIRouter()

HOST = os.getenv('HOST')
API_PORT = os.getenv('API_PORT')


class Urls(Enum):
    ARTICLES = f'http://{HOST}:{API_PORT}/articles/'
    ARTICLES_CREATE = f'http://{HOST}:{API_PORT}/articles/create/'


@router.get('/articles', response_class=HTMLResponse)
async def get_articles(request: Request):
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    articles = await api_request_get(Urls.ARTICLES.value, headers)
    return templates.TemplateResponse(
        "articles.html",
        {"request": request, "articles": articles})


@router.get('/articles/{article_id}', response_class=HTMLResponse)
async def get_article(request: Request, article_id: int):
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    article = await api_request_get(Urls.ARTICLES.value, headers, article_id)
    return templates.TemplateResponse("article.html",
                                      {"request": request, "article": article})


@router.get('/article/create', response_class=HTMLResponse)
async def create_article_form(request: Request):
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    return templates.TemplateResponse("article_create.html",
                                      {"request": request})


@router.post('/article/create', response_class=HTMLResponse)
async def create_article(request: Request,
                         title: str = Form(),
                         content: str = Form()):
    data = {'title': title, 'content': content}
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    await api_request_post(Urls.ARTICLES_CREATE.value, headers, data)
    redirect = RedirectResponse("/", status_code=303)
    return redirect


@router.get('/articles/{article_id}/update', response_class=HTMLResponse)
async def update_article_form(request: Request, article_id: int):
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    return templates.TemplateResponse("article_update.html",
                                      {"request": request})


@router.post('/articles/{article_id}/update', response_class=HTMLResponse)
async def update_article(request: Request,
                         article_id: int,
                         title: str = Form(),
                         content: str = Form()):
    data = {'title': title, 'content': content}
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    article = await api_request_put(
        Urls.ARTICLES.value, headers, article_id, data)

    redirect = create_redirect_with_cookie(
        cookie_value_success='Article was updated',
        cookie_value_fail="You can't change another user's article",
        object=article,
        attribute='title')

    return redirect


@router.get('/articles/{article_id}/delete', response_class=HTMLResponse)
async def delete_article_form(request: Request,
                              article_id: int):
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    return templates.TemplateResponse("article_delete.html",
                                      {"request": request})


@router.post('/articles/{article_id}/delete', response_class=HTMLResponse)
async def delete_article(request: Request,
                         article_id: int):
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    article = await api_request_delete(
        Urls.ARTICLES.value, headers, article_id)

    redirect = create_redirect_with_cookie(
        cookie_value_success='Article was deleted',
        cookie_value_fail="You can't delete another user's article",
        object=article,
        attribute='title')

    return redirect
