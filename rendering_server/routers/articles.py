import aiohttp
import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from rendering_server.utils import templates
from rendering_server.routers.utils import get_headers_with_token
from rendering_server.routers.utils import get_login_redirect
from dotenv import load_dotenv


load_dotenv()

router = APIRouter()

HOST = os.getenv('HOST')


@router.get('/articles', response_class=HTMLResponse)
async def get_articles(request: Request):
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'http://{HOST}:8080/articles',
                headers=headers) as response:
            articles = await response.json()
    return templates.TemplateResponse(
        "articles.html",
        {"request": request, "articles": articles})


@router.get('/articles/{article_id}', response_class=HTMLResponse)
async def get_article(request: Request, article_id: int):
    headers = get_headers_with_token(request)
    if not headers:
        return get_login_redirect()
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'http://{HOST}:8080/articles/{article_id}',
                headers=headers) as response:
            article = await response.json()
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
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f'http://{HOST}:8080/articles/create',
                json=data,
                headers=headers
                ) as response:
            await response.json()
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
    async with aiohttp.ClientSession() as session:
        async with session.put(
                f'http://{HOST}:8080/articles/{article_id}',
                json=data,
                headers=headers
                ) as response:
            article = await response.json()
    redirect = RedirectResponse("/", status_code=303)
    cookie_value = 'Article was updated' if article.get(
        'title') else "You can't change another user's article"
    redirect.set_cookie(key='message', value=cookie_value)
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
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                f'http://{HOST}:8080/articles/{article_id}',
                headers=headers
                ) as response:
            article = await response.json()
    redirect = RedirectResponse("/", status_code=303)
    cookie_value = 'Article was deleted' if article.get(
        'title') else "You can't delete another user's article"
    redirect.set_cookie(key='message', value=cookie_value)
    return redirect
