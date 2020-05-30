from typing import Dict
import jwt

from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from settings import JWT_SECRET_KEY, JWT_ALGORITHM


protected_urls = ('/api', '/beer/add_beer', '/wine/add_wine', '/vodka/add_vodka', '/change_password')


class CheckUserAuthMiddleware(BaseHTTPMiddleware):
    """Миддлварь проверяет токен авторизации"""
    async def dispatch(self, request: Request, call_next, data: Dict[str, str] = None, **kw):
        # передаем в объекте реквеста метку об авторизованности для шаблонов
        request.state.authenticated = False
        response = JSONResponse(
            content={
                'auth_link': '/login_page',
                'success': False,
                'invalid_token': True
            }
        )

        try:
            token = request.cookies['Authorization']
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError, KeyError):
            # токен невалидный или истек
            if not request.url.path.startswith(protected_urls):
                return await call_next(request)
            return RedirectResponse('/login_page') if request.method == 'GET' else response

        request.state.authenticated = True
        request.state.login = payload['login']
        return await call_next(request)
