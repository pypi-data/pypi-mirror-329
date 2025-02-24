from typing import Callable, ParamSpec, TypeVar
from fastapi import APIRouter as FastApiRouter, Depends

T = TypeVar("T")
P = ParamSpec("P")


class ApiRouter(FastApiRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_app_dependency(self, app):
        self._app = app

    def _inject_app_dependency(self, endpoint: Callable[P, T]) -> Callable[P, T]:
        if not self._app:
            raise RuntimeError("App dependency not set.?")

        original_deps = getattr(endpoint, "dependencies", [])

        if not any(dep.dependency == self._app for dep in original_deps):
            endpoint.dependencies = [Depends(self._app)] + original_deps

        return endpoint

    def get(self, path: str, **kwargs):
        def decorator(endpoint: Callable[P, T]) -> Callable[P, T]:
            wrapped_endpoint = self._inject_app_dependency(endpoint)
            return super().get(path, **kwargs)(wrapped_endpoint)
        return decorator

    def post(self, path: str, **kwargs):
        def decorator(endpoint: Callable[P, T]) -> Callable[P, T]:
            wrapped_endpoint = self._inject_app_dependency(endpoint)
            return super().get(path, **kwargs)(wrapped_endpoint)
        return decorator

    def put(self, path: str, **kwargs):
        def decorator(endpoint: Callable[P, T]) -> Callable[P, T]:
            wrapped_endpoint = self._inject_app_dependency(endpoint)
            return super().get(path, **kwargs)(wrapped_endpoint)
        return decorator

    def delete(self, path: str, **kwargs):
        def decorator(endpoint: Callable[P, T]) -> Callable[P, T]:
            wrapped_endpoint = self._inject_app_dependency(endpoint)
            return super().get(path, **kwargs)(wrapped_endpoint)
        return decorator