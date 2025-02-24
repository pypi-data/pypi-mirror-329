import re

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable

from maleo_core.models.dto import BaseDTO

class BaseMiddleware:
    class AuthorizationMiddleware(BaseHTTPMiddleware):
        def __init__(self, app, validate, protected_routes, dispatch = None):
            super().__init__(app, dispatch)
            self.validate = validate
            self.protected_routes = protected_routes

        def normalize_path(self, path: str) -> str:
            """
            Normalize the path to account for dynamic segments and query parameters.
            Example:
                /api/v1/users/123?name=test -> /api/v1/users/{id}
            """
            #* Remove query parameters
            path = re.sub(r'\?.*', '', path)

            #* Replace numeric segments with {id}
            path = re.sub(r'/(?P<digit>\d+)', '/{id}', path)

            #* Replace alphanumeric dynamic segments (excluding static keywords) with {param}
            path = re.sub(r'/(?P<dynamic>[a-zA-Z0-9-]+)', r'/\g<dynamic>', path)

            return path

        async def dispatch(self, request:Request, call_next):
            #* Apply authorization validation
            result: BaseDTO.ValidateResult = self.validate(request)

            #* Normalize the path
            normalized_path = self.normalize_path(request.url.path)
            print("normalized path:", normalized_path)

            #* Check if the normalized path and method require authorization
            if normalized_path in self.protected_routes and request.method in self.protected_routes[normalized_path]:
                if not result.authorized:
                    return result.response

            #* Process the request and get the response
            response = await call_next(request)

            #* Check for an Authorization token
            if result.token:
                response.headers["Authorization"] = f"Bearer {result.token}"

            return response

def add_base_middleware(app:FastAPI, validate:Callable[[Request], Awaitable[BaseDTO]], protected_routes:dict[str: list[str]]):
    app.add_middleware(BaseMiddleware.AuthorizationMiddleware, validate=validate, protected_routes=protected_routes)