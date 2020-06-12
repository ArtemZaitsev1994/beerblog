from typing import Dict
import jwt

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from settings import JWT_SECRET_KEY, JWT_ALGORITHM, AUTH_SERVER_LINK


class CheckUserAuthMiddleware(BaseHTTPMiddleware):
    """Миддлварь проверяет токен авторизации"""
    async def dispatch(self, request: Request, call_next, data: Dict[str, str] = None, **kw):
        # проверяем только запросы к апи, тк все обращения к базе только через апи
        protected_paths = ('/admin/', '/api/')
        if next((False for x in protected_paths if x in request.url.path), True):
            return await call_next(request)

        section = request.headers.get('section')
        response = JSONResponse(
            content={
                'auth_link': AUTH_SERVER_LINK.format(section),
                'success': False,
                'invalid_token': True
            }
        )

        token = request.headers.get('Authorization')
        if not token:
            # нет токена в заголовке
            return response

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            # токен невалидный или истек
            return response

        request.state.authenticated = True
        request.state.login = payload['login']

        if '/admin/' in request.url.path and request.state.login != 'admin':
            return response

        return await call_next(request)
