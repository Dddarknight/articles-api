from fastapi.responses import RedirectResponse


def get_headers_with_token(request):
    token = request.cookies.get('access_token')
    return {'Authorization': f'Bearer {token}'} if token else None


def get_login_redirect():
    response = RedirectResponse("/login", status_code=303)
    response.set_cookie(key='message', value='You need to log in')
    return response
