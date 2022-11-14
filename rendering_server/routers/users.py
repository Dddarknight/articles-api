import os
from enum import Enum
from dotenv import load_dotenv

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from rendering_server.utils import templates
from rendering_server.utils import get_headers_with_token
from rendering_server.utils import api_request_get, api_request_put
from rendering_server.utils import api_request_post_token
from rendering_server.utils import api_request_post, api_request_delete
from rendering_server.utils import create_redirect_with_cookie
from rendering_server.sender import send_to_queue


load_dotenv()

router = APIRouter()

HOST = os.getenv('HOST')
API_PORT = os.getenv('API_PORT')


class Urls(Enum):
    USERS = f'http://{HOST}:{API_PORT}/users/'
    TOKEN = f'http://{HOST}:{API_PORT}/token/'
    SIGNUP = f'http://{HOST}:{API_PORT}/sign-up/'


@router.get('/users', response_class=HTMLResponse)
async def get_users(request: Request):
    users = await api_request_get(Urls.USERS.value)
    return templates.TemplateResponse("users.html",
                                      {"request": request, "users": users})


@router.get('/users/{user_id}', response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    user = await api_request_get(Urls.USERS.value, id=user_id)
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
    token_data = await api_request_post_token(Urls.TOKEN.value, data=data)
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
    await api_request_post(Urls.SIGNUP.value, json=data)

    send_to_queue(
        message=f'A user {username} was registered',
        exchange='registration',
        queue='email_queue')

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

    user = await api_request_put(
        Urls.USERS.value, headers, user_id, data)

    redirect = create_redirect_with_cookie(
        cookie_value_success='User was updated',
        cookie_value_fail="You can't change another user",
        object=user,
        attribute='username')

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

    user = await api_request_delete(
        Urls.USERS.value, headers, user_id)

    redirect = create_redirect_with_cookie(
        cookie_value_success='User was deleted',
        cookie_value_fail="You can't delete another user",
        object=user,
        attribute='username')
    redirect.delete_cookie('access_token')

    return redirect
