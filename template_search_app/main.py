from fastapi import FastAPI

from template_search_app.api.endpoints import router

template_search_app = FastAPI()

template_search_app.include_router(router, prefix='/api/v1')
