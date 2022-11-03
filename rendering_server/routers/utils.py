import aiohttp

from fastapi.responses import RedirectResponse


def get_headers_with_token(request):
    token = request.cookies.get('access_token')
    return {'Authorization': f'Bearer {token}'} if token else None


def get_login_redirect():
    response = RedirectResponse("/login", status_code=303)
    response.set_cookie(key='message', value='You need to log in')
    return response


async def api_request_get(url, headers={}, id=''):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{url}{id}',
                headers=headers) as response:
            data = await response.json()
    return data


async def api_request_post(url, headers={}, json=''):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f'{url}',
                json=json,
                headers=headers) as response:
            data = await response.json()
    return data


async def api_request_post_token(url, headers={}, data=''):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f'{url}',
                data=data,
                headers=headers) as response:
            data = await response.json()
    return data


async def api_request_put(url, headers={}, id='', json=''):
    async with aiohttp.ClientSession() as session:
        async with session.put(
                f'{url}{id}',
                json=json,
                headers=headers) as response:
            data = await response.json()
    return data


async def api_request_delete(url, headers={}, id=''):
    async with aiohttp.ClientSession() as session:
        async with session.delete(
                f'{url}{id}',
                headers=headers) as response:
            data = await response.json()
    return data


def create_redirect_with_cookie(cookie_value_success,
                                cookie_value_fail,
                                object,
                                attribute):
    redirect = RedirectResponse("/", status_code=303)
    cookie_value = cookie_value_success if object.get(
        attribute) else cookie_value_fail
    redirect.set_cookie(key='message', value=cookie_value)
    return redirect
