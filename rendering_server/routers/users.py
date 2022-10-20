import aiohttp
import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from rendering_server.utils import templates
from rendering_server.routers.utils import get_headers_with_token
from dotenv import load_dotenv
from rendering_server.mail_service.sender import send_to_queue
from rendering_server.mail_service.listener import listen_to_queue, get_moderators_emails


load_dotenv()

router = APIRouter()

HOST = os.getenv('HOST')


@router.get('/users', response_class=HTMLResponse)
async def get_users(request: Request):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'http://{HOST}:8080/users') as response:
            users = await response.json()
    return templates.TemplateResponse("users.html",
                                      {"request": request, "users": users})


@router.get('/users/{user_id}', response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'http://{HOST}:8080/users/{user_id}'
                ) as response:
            user = await response.json()
    return templates.TemplateResponse("user.html",
                                      {"request": request, "user": user})


@router.get('/login', response_class=HTMLResponse)
def login_form(request: Request):
    if request.cookies.get('message'):
        response = templates.TemplateResponse(
            "login.html",
            {"request": request,
             "message": request.cookies['message']})
        response.delete_cookie('message')
        return response
    return templates.TemplateResponse("login.html",
                                      {"request": request})


@router.post('/login', response_class=HTMLResponse)
async def login(username: str = Form(), password: str = Form()):
    data = {'username': username, 'password': password}
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{HOST}:8080/token',
                                data=data) as response:
            token_data = await response.json()
            token = token_data['access_token']
    redirect = RedirectResponse("/", status_code=303)
    redirect.set_cookie(key='access_token', value=token, expires=900)
    return redirect


@router.get('/logout', response_class=HTMLResponse)
def logout(request: Request):
    redirect = RedirectResponse("/", status_code=303)
    redirect.delete_cookie('access_token')
    return redirect


@router.get('/sign-up', response_class=HTMLResponse)
def sign_up_form(request: Request):
    return templates.TemplateResponse("sign-up.html",
                                      {"request": request})


@router.post('/sign-up', response_class=HTMLResponse)
async def sign_up(username: str = Form(),
                  email: str = Form(),
                  full_name: str = Form(),
                  password: str = Form()):
    data = {'username': username,
            'email': email,
            'full_name': full_name,
            'password': password}
    async with aiohttp.ClientSession() as session:
        async with session.post(f'http://{HOST}:8080/sign-up',
                                json=data) as response:
            await response.json()
    send_to_queue()
    listen_to_queue()
    redirect = RedirectResponse("/login", status_code=303)
    return redirect


@router.get('/users/{user_id}/update', response_class=HTMLResponse)
async def update_user_form(request: Request, user_id: int):
    headers = get_headers_with_token(request)
    if not headers:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("user_update.html",
                                      {"request": request})


@router.post('/users/{user_id}/update', response_class=HTMLResponse)
async def update_user(request: Request,
                      user_id: int,
                      username: str = Form(),
                      email: str = Form(),
                      full_name: str = Form(),
                      password: str = Form()):
    data = {'username': username,
            'email': email,
            'full_name': full_name,
            'password': password}
    headers = get_headers_with_token(request)
    if not headers:
        return RedirectResponse("/login", status_code=303)
    async with aiohttp.ClientSession() as session:
        async with session.put(
                f'http://{HOST}:8080/users/{user_id}',
                json=data,
                headers=headers
                ) as response:
            user = await response.json()
    redirect = RedirectResponse("/", status_code=303)
    cookie_value = 'User was updated' if user.get(
        'username') else "You can't change another user"
    redirect.set_cookie(key='message', value=cookie_value)
    return redirect


@router.get('/users/{user_id}/delete', response_class=HTMLResponse)
async def delete_article_form(request: Request,
                              user_id: int):
    headers = get_headers_with_token(request)
    if not headers:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("user_delete.html",
                                      {"request": request})


@router.post('/users/{user_id}/delete', response_class=HTMLResponse)
async def delete_article(request: Request,
                         user_id: int):
    headers = get_headers_with_token(request)
    if not headers:
        return RedirectResponse("/login", status_code=303)
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                f'http://{HOST}:8080/users/{user_id}',
                headers=headers
                ) as response:
            user = await response.json()
    redirect = RedirectResponse("/", status_code=303)
    cookie_value = 'User was deleted' if user.get(
        'username') else "You can't delete another user"
    redirect.set_cookie(key='message', value=cookie_value)
    redirect.delete_cookie('access_token')
    return redirect


# @router.get('/moderators', response_class=HTMLResponse)
# async def get_m(request: Request):
#     emails = await get_moderators_emails()
#     return templates.TemplateResponse("moderators.html",
#                                       {"request": request, "emails": emails})
